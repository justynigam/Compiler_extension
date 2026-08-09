package com.codedock.compiler;

public interface LanguageCompiler {

    String getLanguage();

    String getSourceFileName();

    String getSourceFileExtension();

    boolean isCompiled();

    String getCompileCommand();

    String getRunCommand();

    String getDockerImage();
}