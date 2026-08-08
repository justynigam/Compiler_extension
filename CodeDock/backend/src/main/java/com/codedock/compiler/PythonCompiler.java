package com.codedock.compiler;

import org.springframework.stereotype.Component;

@Component
public class PythonCompiler implements LanguageCompiler {

    @Override
    public String getLanguage() {
        return "python";
    }

    @Override
    public String getSourceFileName() {
        return "main.py";
    }

    @Override
    public String getSourceFileExtension() {
        return ".py";
    }

    @Override
    public boolean isCompiled() {
        return false;
    }

    @Override
    public String getCompileCommand() {
        return null;
    }

    @Override
    public String getRunCommand() {
        return "python3 main.py";
    }

    @Override
    public String getDockerImage() {
        return "codedock-python:latest";
    }
}