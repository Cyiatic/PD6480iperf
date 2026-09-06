// Minimal software-video libretro test host. No GPU/window or console access.
#include <windows.h>
#include "libretro.h"
#include <cstdint>
#include <cstdio>
#include <cstdarg>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <filesystem>
#include <string>
#include <map>
#include <vector>
#include <chrono>
#include "controller_input.h"
#include "ram_counter_watch.h"

static std::map<std::string,std::string> options;
static std::string directory;
static unsigned pixel_format = RETRO_PIXEL_FORMAT_0RGB1555;
static bool shutdown_requested = false;
static unsigned frame_index = 0, video_width = 0, video_height = 0, video_count = 0;
static std::vector<uint8_t> image;
static std::vector<InputRange> inputs;
static unsigned connected_ports = 1;
struct RamWrite { unsigned frame, address, value; };
static std::vector<RamWrite> ram_writes;

static void core_log(enum retro_log_level level, const char *format, ...) {
  if (level < RETRO_LOG_INFO) return;
  va_list args; va_start(args,format); vfprintf(stderr,format,args); va_end(args);
}
static bool environment(unsigned cmd, void *data) {
  switch(cmd) {
    case RETRO_ENVIRONMENT_GET_LOG_INTERFACE:
      ((retro_log_callback*)data)->log = core_log; return true;
    case RETRO_ENVIRONMENT_GET_SYSTEM_DIRECTORY:
    case RETRO_ENVIRONMENT_GET_SAVE_DIRECTORY:
      *(const char**)data = directory.c_str(); return true;
    case RETRO_ENVIRONMENT_GET_CAN_DUPE: *(bool*)data = true; return true;
    case RETRO_ENVIRONMENT_SET_PIXEL_FORMAT:
      pixel_format = *(unsigned*)data; return pixel_format <= RETRO_PIXEL_FORMAT_RGB565;
    case RETRO_ENVIRONMENT_GET_CORE_OPTIONS_VERSION: *(unsigned*)data = 0; return true;
    case RETRO_ENVIRONMENT_SET_VARIABLES: {
      for(auto *v=(retro_variable*)data; v && v->key; ++v) {
        if(options.count(v->key)) {
          printf("OPTION %s=%s\n",v->key,options[v->key].c_str());
        } else {
          std::string values=v->value ? v->value : "";
          auto semi=values.find("; ");
          if(semi!=std::string::npos) values=values.substr(semi+2);
          options[v->key]=values.substr(0,values.find('|'));
        }
      }
      return true;
    }
    case RETRO_ENVIRONMENT_GET_VARIABLE: {
      auto *v=(retro_variable*)data; auto it=options.find(v->key);
      v->value=it==options.end()?nullptr:it->second.c_str(); return v->value!=nullptr;
    }
    case RETRO_ENVIRONMENT_GET_VARIABLE_UPDATE: *(bool*)data=false; return true;
    case RETRO_ENVIRONMENT_GET_INPUT_BITMASKS: return true;
    case RETRO_ENVIRONMENT_GET_LANGUAGE: *(unsigned*)data=RETRO_LANGUAGE_ENGLISH; return true;
    case RETRO_ENVIRONMENT_GET_AUDIO_VIDEO_ENABLE: *(int*)data=3; return true;
    case RETRO_ENVIRONMENT_SET_GEOMETRY:
    case RETRO_ENVIRONMENT_SET_SYSTEM_AV_INFO:
    case RETRO_ENVIRONMENT_SET_CONTROLLER_INFO:
    case RETRO_ENVIRONMENT_SET_INPUT_DESCRIPTORS:
    case RETRO_ENVIRONMENT_SET_PERFORMANCE_LEVEL:
    case RETRO_ENVIRONMENT_SET_SUPPORT_NO_GAME: return true;
    case RETRO_ENVIRONMENT_SHUTDOWN: shutdown_requested=true; return true;
    case RETRO_ENVIRONMENT_SET_HW_RENDER:
      fprintf(stderr,"Hardware-render request rejected: software-only host\n"); return false;
    default: return false;
  }
}
static void video(const void *data,unsigned width,unsigned height,size_t pitch) {
  if(!data || data==RETRO_HW_FRAME_BUFFER_VALID) return;
  if(width>4096 || height>4096) { shutdown_requested=true; return; }
  video_width=width; video_height=height; ++video_count;
  image.resize(size_t(width)*height*3);
  for(unsigned y=0;y<height;++y) for(unsigned x=0;x<width;++x) {
    auto *row=(const uint8_t*)data+y*pitch;
    uint8_t r,g,b;
    if(pixel_format==RETRO_PIXEL_FORMAT_XRGB8888) {
      uint32_t p; memcpy(&p,row+x*4,4); r=p>>16;g=p>>8;b=p;
    } else {
      uint16_t p; memcpy(&p,row+x*2,2);
      b=(p&31)*255/31;
      if(pixel_format==RETRO_PIXEL_FORMAT_RGB565) {r=((p>>11)&31)*255/31;g=((p>>5)&63)*255/63;}
      else {r=((p>>10)&31)*255/31;g=((p>>5)&31)*255/31;}
    }
    size_t i=(size_t(y)*width+x)*3;image[i]=r;image[i+1]=g;image[i+2]=b;
  }
}
static void audio(int16_t,int16_t) {}
static size_t audio_batch(const int16_t*,size_t frames) {return frames;}
static void input_poll() {}
static int16_t input_state(unsigned port,unsigned device,unsigned index,unsigned id) {
  auto value=controller_input(inputs,frame_index,port,connected_ports);
  if(device==RETRO_DEVICE_JOYPAD) return id==RETRO_DEVICE_ID_JOYPAD_MASK ? int16_t(value.mask) : (id<16 ? ((value.mask>>id)&1) : 0);
  if(device==RETRO_DEVICE_ANALOG && index==RETRO_DEVICE_INDEX_ANALOG_LEFT) return id==0 ? value.x : (id==1 ? value.y : 0);
  return 0;
}
static std::vector<char> read_file(const std::string &path) {
  std::ifstream in(path,std::ios::binary);
  if(!in) throw std::runtime_error("Cannot read "+path);
  return {std::istreambuf_iterator<char>(in),std::istreambuf_iterator<char>()};
}
static void write_file(const std::string &path,const void *data,size_t length) {
  std::ofstream out(path,std::ios::binary); out.write((const char*)data,length);
  if(!out) throw std::runtime_error("Cannot write "+path);
}
static void snapshot(unsigned frame) {
  if(image.empty()) return;
  std::string path=directory+"/frame-"+std::to_string(frame)+".ppm";
  std::ofstream out(path,std::ios::binary);
  out<<"P6\n"<<video_width<<" "<<video_height<<"\n255\n";
  out.write((const char*)image.data(),image.size());
}
template<class T> static T symbol(HMODULE lib,const char*name) {
  auto p=GetProcAddress(lib,name); if(!p) throw std::runtime_error(std::string("Missing ")+name);
  return reinterpret_cast<T>(p);
}
#define LOAD(name) auto name##_p=symbol<decltype(&name)>(lib,#name)
int main(int argc,char **argv) try {
  setvbuf(stdout,nullptr,_IONBF,0);
  if(argc<5) {fprintf(stderr,"host CORE ROM OUTDIR FRAMES [CPU] [INPUT.txt|-] [STATE|-] [SAVE|-] [eeprom-header|-] [WRITES|-] [CONNECTED_MASK] [WATCH_COUNTER:GATE:VALUE|-]\n");return 2;}
  directory=std::filesystem::absolute(argv[3]).string();
  // Existing runners create their input/log files before invoking the host.
  // Accept that setup, but never overwrite an earlier emulation result.
  if(std::filesystem::exists(directory)) for(const auto &entry:std::filesystem::directory_iterator(directory)) {
    auto name=entry.path().filename().string();
    if(name=="state.bin" || name=="rdram-last.bin" || name=="save-memory.bin" ||
       name.rfind("watch-",0)==0 || (name.rfind("frame-",0)==0 && entry.path().extension()==".ppm"))
      throw std::runtime_error("Output directory contains prior emulation results");
  }
  std::filesystem::create_directories(directory);
  unsigned frames=std::stoul(argv[4]);
  RamCounterWatch watch;
  if(argc>12 && strcmp(argv[12],"-")) {
    watch=RamCounterWatch::parse(argv[12]);
    printf("READ-ONLY WATCH counter=%08x gate=%08x value=%u limit=%u\n",watch.address,watch.gate_address,watch.gate_value,watch.limit);
  }
  if(argc>11) {
    size_t used=0; unsigned long mask=std::stoul(argv[11],&used,0);
    if(used!=strlen(argv[11]) || mask>15) throw std::runtime_error("Connected controller mask must be 0..15");
    connected_ports=unsigned(mask);
  }
  options["parallel-n64-gfxplugin"]="angrylion";
  options["parallel-n64-rspplugin"]="cxd4";
  options["parallel-n64-cpucore"]=argc>5?argv[5]:"cached_interpreter";
  // Despite the legacy key name, current cores use enabled = 8 MiB.
  options["parallel-n64-disable_expmem"]="enabled";
  options["parallel-n64-OverrideSaveType"]="EEPROM_16KB";
  options["parallel-n64-angrylion-multithread"]="4";
  options["parallel-n64-angrylion-overscan"]="disabled";
  if(argc>6 && strcmp(argv[6],"-")) {
    std::ifstream file(argv[6]);
    if(!file) throw std::runtime_error("Cannot read controller input");
    inputs=parse_inputs(file);
  }
  if(argc>10 && strcmp(argv[10],"-")) {
    std::ifstream file(argv[10]);RamWrite op;
    while(file>>std::dec>>op.frame>>std::hex>>op.address>>op.value) {
      if(op.address<0x80000000 || op.address>0x807ffffc || (op.address&3))
        throw std::runtime_error("RAM write must be aligned within KSEG0 RDRAM");
      ram_writes.push_back(op);
    }
  }
  HMODULE lib=LoadLibraryA(argv[1]);
  if(!lib) {fprintf(stderr,"LoadLibrary error %lu\n",GetLastError());return 3;}
  LOAD(retro_set_environment);LOAD(retro_set_video_refresh);LOAD(retro_set_audio_sample);
  LOAD(retro_set_audio_sample_batch);LOAD(retro_set_input_poll);LOAD(retro_set_input_state);
  LOAD(retro_init);LOAD(retro_deinit);LOAD(retro_load_game);LOAD(retro_unload_game);
  LOAD(retro_run);LOAD(retro_get_system_info);LOAD(retro_get_memory_data);LOAD(retro_get_memory_size);
  LOAD(retro_set_controller_port_device);LOAD(retro_serialize_size);LOAD(retro_serialize);LOAD(retro_unserialize);
  retro_set_environment_p(environment);retro_set_video_refresh_p(video);
  retro_set_audio_sample_p(audio);retro_set_audio_sample_batch_p(audio_batch);
  retro_set_input_poll_p(input_poll);retro_set_input_state_p(input_state);
  retro_init_p();
  retro_system_info info{};retro_get_system_info_p(&info);
  printf("CORE %s %s fullpath=%d\n",info.library_name,info.library_version,info.need_fullpath);
  auto rom=read_file(argv[2]);
  if(argc>9 && !strcmp(argv[9],"eeprom-header")) {
    // This core's current rom.c does not apply the advertised save override.
    // Adapter only: use its documented homebrew header to select 16-Kbit EEPROM.
    // The on-disk candidate is untouched; no code, assets, or VI bytes change.
    rom.at(0x3c)='E';rom.at(0x3d)='D';rom.at(0x3f)=0x20;
    printf("TEST ADAPTER: in-memory ED/16K EEPROM header; disk ROM unchanged\n");
  }
  retro_game_info game{argv[2],rom.data(),rom.size(),nullptr};
  if(!retro_load_game_p(&game)) {fprintf(stderr,"Load game failed\n");return 4;}
  for(unsigned port=0;port<4;++port) retro_set_controller_port_device_p(port,(connected_ports&(1u<<port))?RETRO_DEVICE_JOYPAD:RETRO_DEVICE_NONE);
  printf("CONTROLLERS mask=%u input_ranges=%zu\n",connected_ports,inputs.size());
  if(argc>8 && strcmp(argv[8],"-")) {
    auto save=read_file(argv[8]);auto size=retro_get_memory_size_p(RETRO_MEMORY_SAVE_RAM);
    // libretro_memory.h: the 2 KiB EEPROM is the first save_memory_data member.
    printf("SAVE available=%zu supplied=%zu\n",size,save.size());
    if(size==save.size() || (size==296960 && save.size()==2048))
      memcpy(retro_get_memory_data_p(RETRO_MEMORY_SAVE_RAM),save.data(),save.size());
    else throw std::runtime_error("Unrecognized save memory size");
  }
  if(argc>7 && strcmp(argv[7],"-")) {
    // The core creates its emulation thread and memory on the first run.
    retro_run_p();
    auto state=read_file(argv[7]);
    if(!retro_unserialize_p(state.data(),state.size())) throw std::runtime_error("State restore failed");
    if(watch.address) {
      watch.prime((const uint8_t*)retro_get_memory_data_p(RETRO_MEMORY_SYSTEM_RAM),retro_get_memory_size_p(RETRO_MEMORY_SYSTEM_RAM));
      printf("WATCH restored baseline=%u (historical counts are not new events)\n",watch.previous);
    }
  }
  auto start=std::chrono::steady_clock::now();
  for(frame_index=0;frame_index<frames && !shutdown_requested;++frame_index) {
    for(auto op:ram_writes) if(op.frame==frame_index) {
      auto *ram=(uint8_t*)retro_get_memory_data_p(RETRO_MEMORY_SYSTEM_RAM);
      if(!ram) throw std::runtime_error("No RAM for requested test write");
      memcpy(ram+(op.address&0x7fffff),&op.value,4);
      printf("TEST RAM WRITE frame=%u address=%08x value=%08x\n",frame_index,op.address,op.value);
    }
    retro_run_p();
    if(watch.address) {
      auto *watched_ram=(const uint8_t*)retro_get_memory_data_p(RETRO_MEMORY_SYSTEM_RAM);
      auto watched_size=retro_get_memory_size_p(RETRO_MEMORY_SYSTEM_RAM);
      uint32_t before=0,after=0;
      if(watch.sample(watched_ram,watched_size,before,after)) {
        auto stem=directory+"/watch-"+std::to_string(watch.captures)+"-frame-"+std::to_string(frame_index+1);
        write_file(stem+"-rdram.bin",watched_ram,watched_size);
        std::vector<char> watched_state(retro_serialize_size_p());
        bool saved=!watched_state.empty() && retro_serialize_p(watched_state.data(),watched_state.size());
        if(saved) write_file(stem+"-state.bin",watched_state.data(),watched_state.size());
        snapshot(frame_index+1);
        printf("WATCH frame=%u event=%u counter=%08x before=%u after=%u state=%d\n",frame_index+1,watch.captures,watch.address,before,after,saved);
      }
    }
    if((frame_index+1)%300==0) {
      snapshot(frame_index+1);
      double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
      printf("FRAME %u video=%u %ux%u seconds=%.1f\n",frame_index+1,video_count,video_width,video_height,elapsed);
      auto ram=retro_get_memory_data_p(RETRO_MEMORY_SYSTEM_RAM);auto size=retro_get_memory_size_p(RETRO_MEMORY_SYSTEM_RAM);
      if(ram && size) write_file(directory+"/rdram-last.bin",ram,size);
    }
  }
  snapshot(frame_index);
  auto ram=retro_get_memory_data_p(RETRO_MEMORY_SYSTEM_RAM);auto ram_size=retro_get_memory_size_p(RETRO_MEMORY_SYSTEM_RAM);
  if(ram && ram_size) write_file(directory+"/rdram-last.bin",ram,ram_size);
  auto save=retro_get_memory_data_p(RETRO_MEMORY_SAVE_RAM);auto save_size=retro_get_memory_size_p(RETRO_MEMORY_SAVE_RAM);
  if(save && save_size) write_file(directory+"/save-memory.bin",save,save_size);
  std::vector<char> state(retro_serialize_size_p());
  if(!state.empty() && retro_serialize_p(state.data(),state.size())) write_file(directory+"/state.bin",state.data(),state.size());
  printf("DONE frames=%u ram=%zu save=%zu state=%zu\n",frame_index,ram_size,save_size,state.size());
  retro_unload_game_p();retro_deinit_p();FreeLibrary(lib);
  return 0;
} catch(const std::exception&e) {fprintf(stderr,"ERROR %s\n",e.what());return 10;}
