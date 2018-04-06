#include "../include/settings_parser.hpp"


SettingsParser::SettingsParser(std::string fname) {
    __fname = fname;
}

void SettingsParser::parseSettings() {
    std::ifstream fin(__fname);
    std::string key;
    std::string value;
    while(fin >> key && fin >> value) {
        __keysValues.insert(
            std::pair<std::string, std::string>(std::make_pair(key, value)));
    }
    fin.close();
    return;
}

std::string SettingsParser::getProperty(std::string key) {
    return __keysValues[key];
}
