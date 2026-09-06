#pragma once
#include <cstdint>
#include <cstddef>
#include <stdexcept>
#include <string>

// Read-only observer for this host's word-swapped, 8 MiB libretro RDRAM.
// A gate prevents sampling an uninitialised counter during boot/loading.
struct RamCounterWatch {
  uint32_t address=0, gate_address=0, gate_value=0, previous=0;
  unsigned captures=0;
  static constexpr unsigned limit=8;

  static uint32_t number(const std::string &text) {
    if(text.empty() || text[0]=='-' || text[0]=='+' || text[0]==' ')
      throw std::runtime_error("Invalid RAM watch number");
    size_t used=0;
    auto value=std::stoull(text,&used,0);
    if(used!=text.size() || value>UINT32_MAX)
      throw std::runtime_error("Invalid RAM watch number");
    return uint32_t(value);
  }
  static bool valid_address(uint32_t value) {
    return value>=0x80000000u && value<=0x807ffffcu && !(value&3);
  }
  static RamCounterWatch parse(const std::string &text) {
    auto first=text.find(':');
    auto second=first==std::string::npos ? first : text.find(':',first+1);
    if(first==std::string::npos || second==std::string::npos || text.find(':',second+1)!=std::string::npos)
      throw std::runtime_error("RAM watch requires COUNTER:GATE:VALUE");
    RamCounterWatch watch;
    watch.address=number(text.substr(0,first));
    watch.gate_address=number(text.substr(first+1,second-first-1));
    watch.gate_value=number(text.substr(second+1));
    if(!valid_address(watch.address) || !valid_address(watch.gate_address))
      throw std::runtime_error("RAM watch addresses must be aligned within KSEG0 RDRAM");
    return watch;
  }
  static uint32_t read_word(const uint8_t *ram,uint32_t address) {
    auto p=ram+(address&0x7fffff);
    return uint32_t(p[0]) | uint32_t(p[1])<<8 | uint32_t(p[2])<<16 | uint32_t(p[3])<<24;
  }
  void prime(const uint8_t *ram,size_t size) {
    if(!address) return;
    if(!ram || size!=0x800000) throw std::runtime_error("Cannot prime RAM watch without 8 MiB RDRAM");
    previous=read_word(ram,gate_address)==gate_value ? read_word(ram,address) : 0;
  }
  bool sample(const uint8_t *ram,size_t size,uint32_t &before,uint32_t &after) {
    if(!address || !ram) return false;
    if(size!=0x800000) throw std::runtime_error("RAM watch requires exactly 8 MiB RDRAM");
    if(read_word(ram,gate_address)!=gate_value) { previous=0; return false; }
    before=previous;
    after=read_word(ram,address);
    previous=after;
    if(after<=before || captures>=limit) return false;
    ++captures;
    return true;
  }
};
