package com.codedock.compiler;

import org.springframework.stereotype.Component;

@Component
public class CCompiler implements LanguageCompiler {

    @Override
    public String getLanguage() {
        return "c";
    }

    @Override
    public String getSourceFileName() {
        return "main.c";
    }

    @Override
    public String getSourceFileExtension() {
        return ".c";
    }

    @Override
    public boolean isCompiled() {
        return true;
    }

    @Override
    public String getCompileCommand() {
        return "gcc main.c -o main";
    }

    @Override
    public String getRunCommand() {
        return "./main";
    }

    @Override
    public String getDockerImage() {
        return "codedock-c:latest";
    }
}