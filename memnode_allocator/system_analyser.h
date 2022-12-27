#ifndef __SYSTEM_ANALYSER_H__
#define __SYSTEM_ANALYSER_H__
#include <string>
class SystemAnalyser
{
    public:
        SystemAnalyser();
        virtual void RunCommand(const char * command);
        virtual void StoreOutput(std::string& result);
        virtual void DisplayOutput();
        virtual ~SystemAnalyser();
};
#endif