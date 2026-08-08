package com.codedock.compiler;

import org.springframework.stereotype.Component;

@Component
public class CppCompiler implements LanguageCompiler {

    @Override
    public String getLanguage() {
        return "cpp";
    }

    @Override
    public String getSourceFileName() {
        return "main.cpp";
    }

    @Override
    public String getSourceFileExtension() {
        return ".cpp";
    }

    @Override
    public boolean isCompiled() {
        return true;
    }

    @Override
    public String getCompileCommand() {
        return "g++ main.cpp -o main";
    }

    @Override
    public String getRunCommand() {
        return "./main";
    }

    @Override
    public String getDockerImage() {
        return "codedock-cpp:latest";
    }
}