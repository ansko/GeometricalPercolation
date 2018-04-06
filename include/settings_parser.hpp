#pragma once

#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <vector>


class SettingsParser
{
public:
    SettingsParser(std::string fname);
    void parseSettings();
    std::string getProperty(std::string key);
private:
    std::string __fname;
    std::map<std::string, std::string> __keysValues;
};
