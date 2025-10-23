#ifndef KEYS_H
#define KEYS_H

#include <map>
#include <string>


std::map<std::string, std::string> special_keys = {
  {"01110", " "},
  {"11100", "."},
  {"11110", ","}
};

std::string order[30] = {
  "e", "t", "a", "o", "i", "n", "s", "r", "h", "d",
  "l", "u", "c", "m", "f", "y", "w", "g", "p", "b",
  "v", "k", "x", "q", "j", "z", "(", ")","-","+"
};

#endif