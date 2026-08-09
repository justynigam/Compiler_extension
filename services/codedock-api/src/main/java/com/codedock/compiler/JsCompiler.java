package com.codedock.compiler;

import org.springframework.stereotype.Component;

@Component
public class JsCompiler implements LanguageCompiler {

    @Override
    public String getLanguage() {
        return "javascript";
    }

    @Override
    public String getSourceFileName() {
        return "script.js";
    }

    @Override
    public String getSourceFileExtension() {
        return ".js";
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
        return "node script.js";
    }

    @Override
    public String getDockerImage() {
        return "codedock-js:latest";
    }
}