// Test frontend only. No ROM code or game-state writes.
#pragma once
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

struct InputRange { unsigned begin, end, mask; int x, y; unsigned port = 0; };
struct InputValue { unsigned mask = 0; int x = 0, y = 0; };

inline std::vector<InputRange> parse_inputs(std::istream &file) {
  std::vector<InputRange> result;
  std::string line;
  while (std::getline(file, line)) {
    line = line.substr(0, line.find('#'));
    std::istringstream values(line);
    values >> std::ws;
    if (values.eof()) continue;
    long long begin, end, mask, x, y, port = 0;
    if (!(values >> begin >> end >> mask >> x >> y))
      throw std::runtime_error("Malformed controller input line");
    values >> std::ws;
    if (!values.eof() && !(values >> port))
      throw std::runtime_error("Invalid controller port");
    values >> std::ws;
    if (!values.eof() || begin < 0 || end <= begin || end > 0xffffffffLL ||
        mask < 0 || mask > 0xffff || x < -32768 || x > 32767 ||
        y < -32768 || y > 32767 || port < 0 || port > 3)
      throw std::runtime_error("Controller input outside supported range");
    result.push_back({unsigned(begin), unsigned(end), unsigned(mask), int(x), int(y), unsigned(port)});
  }
  return result;
}

inline InputValue controller_input(const std::vector<InputRange> &ranges,
                                   unsigned frame, unsigned port, unsigned connected) {
  InputValue value;
  if (port > 3 || !(connected & (1u << port))) return value;
  for (const auto &range : ranges) {
    if (range.port == port && frame >= range.begin && frame < range.end) {
      value.mask |= range.mask;
      value.x = range.x;
      value.y = range.y;
    }
  }
  return value;
}
