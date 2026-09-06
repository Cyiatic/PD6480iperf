#include "ram_counter_watch.h"
#include <cassert>
#include <cstdio>
#include <vector>

int main() {
  auto watch=RamCounterWatch::parse("0x80000000:0x807ffffc:3");
  std::vector<uint8_t> ram(0x800000,0);
  auto put=[&](size_t offset,uint32_t value) {
    for(unsigned i=0;i<4;++i) ram[offset+i]=uint8_t(value>>(8*i));
  };
  uint32_t before=0,after=0;
  put(0,99);
  assert(!watch.sample(ram.data(),ram.size(),before,after));
  put(0x7ffffc,3); put(0,0);
  assert(!watch.sample(ram.data(),ram.size(),before,after));
  put(0,1);
  const auto unchanged=ram;
  assert(watch.sample(ram.data(),ram.size(),before,after) && before==0 && after==1);
  assert(ram==unchanged);
  assert(!watch.sample(ram.data(),ram.size(),before,after));
  put(0,0); // Counter reset is not an increment.
  assert(!watch.sample(ram.data(),ram.size(),before,after));
  for(unsigned i=1;i<=9;++i) {
    put(0,i);
    assert(watch.sample(ram.data(),ram.size(),before,after)==(i<=7));
  }
  assert(watch.captures==8);
  auto restored=RamCounterWatch::parse("0x80000000:0x807ffffc:3");
  restored.prime(ram.data(),ram.size());
  assert(restored.previous==9 && restored.captures==0);
  assert(!restored.sample(ram.data(),ram.size(),before,after));
  put(0,10);
  assert(restored.sample(ram.data(),ram.size(),before,after) && before==9 && after==10);
  put(0x7ffffc,2);
  assert(!watch.sample(ram.data(),ram.size(),before,after) && watch.previous==0);
  for(const char *bad:{"", "0x80000000", "0x80000000:3", "0x80000000:0x80000004:3:4",
      "0x80000001:0x80000004:3", "0x7ffffffc:0x80000004:3", "0x80800000:0x80000004:3",
      "0x80000000:0xa0000000:3", "0x80000000:0x80000004:-1", "0x80000000:0x80000004:4294967296",
      "0x80000000:0x80000004:3junk", "0x80000000:0x80000004:"}) {
    bool rejected=false;
    try { RamCounterWatch::parse(bad); } catch(const std::exception&) {rejected=true;}
    assert(rejected);
  }
  bool rejected=false;
  try { watch.sample(ram.data(),0x400000,before,after); } catch(const std::exception&) {rejected=true;}
  assert(rejected);
  puts("RAM watch: endian/gate/reset/read-only/cap/range/malformed tests passed");
}
