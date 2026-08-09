package com.codedock.compiler;

import org.springframework.stereotype.Component;

@Component
public class JavaCompiler implements LanguageCompiler {

    @Override
    public String getLanguage() {
        return "java";
    }

    @Override
    public String getSourceFileName() {
        return "Main.java";
    }

    @Override
    public String getSourceFileExtension() {
        return ".java";
    }

    @Override
    public boolean isCompiled() {
        return true;
    }

    @Override
    public String getCompileCommand() {
        return "javac Main.java";
    }

    @Override
    public String getRunCommand() {
        return "java Main";
    }

    @Override
    public String getDockerImage() {
        return "codedock-java:latest";
    }
}