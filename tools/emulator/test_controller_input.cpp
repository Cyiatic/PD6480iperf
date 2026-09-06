#include "controller_input.h"
#include <cassert>
#include <iostream>

int main() {
  std::istringstream text("10 20 1 100 -200\n10 20 2 -300 400 1\n"
                         "10 20 4 500 -600 2\n10 20 8 -700 800 3\n"
                         "12 16 16 10 20 0 # overlay\n");
  auto ranges=parse_inputs(text);
  for(unsigned frame=0;frame<30;++frame) for(unsigned port=0;port<8;++port)
    for(unsigned connected=0;connected<16;++connected) {
      auto value=controller_input(ranges,frame,port,connected);
      bool active=port<4 && (connected&(1u<<port)) && frame>=10 && frame<20;
      unsigned expected=active?(1u<<port):0;
      if(active && port==0 && frame>=12 && frame<16) expected|=16;
      assert(value.mask==expected);
      if(!active) assert(value.x==0 && value.y==0);
      else if(port==1) assert(value.x==-300 && value.y==400);
      else if(port==2) assert(value.x==500 && value.y==-600);
      else if(port==3) assert(value.x==-700 && value.y==800);
      else if(frame>=12 && frame<16) assert(value.x==10 && value.y==20);
      else assert(value.x==100 && value.y==-200);
    }
  for(const auto &bad : {"0 1 1 0", "0 1 1 0 0 4", "0 1 1 0 0 -1",
      "0 1 65536 0 0", "0 1 1 32768 0", "0 1 1 0 -32769",
      "1 1 1 0 0", "-1 1 1 0 0", "0 4294967296 1 0 0",
      "0 1 1 0 0 word", "0 1 1 0 0 0 extra"}) {
    bool rejected=false;
    try {std::istringstream input(bad);parse_inputs(input);} catch(const std::runtime_error &) {rejected=true;}
    assert(rejected);
  }
  std::cout<<"PASS: 3840 frame/port/presence cases, independent analog/button inputs, legacy port0 and 11 malformed input cases\n";
}
