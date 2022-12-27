#include <iostream>
#include <string>
#include <memory>
#include <array>

#include "system_analyser.h"

SystemAnalyser::SystemAnalyser()
{
}
void SystemAnalyser::RunCommand(const char * command)
{
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(command, "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    std::cout << result << std::endl;
}
void SystemAnalyser::StoreOutput(std::string& result)
{
}
void SystemAnalyser::DisplayOutput()
{
}
SystemAnalyser::~SystemAnalyser()
{
}