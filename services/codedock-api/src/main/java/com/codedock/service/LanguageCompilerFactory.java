package com.codedock.service;

import com.codedock.compiler.*;
import com.codedock.exception.InvalidLanguageException;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class LanguageCompilerFactory {

    private final Map<String, LanguageCompiler> compilers = new HashMap<>();

    public LanguageCompilerFactory(JavaCompiler javaCompiler,
                                   PythonCompiler pythonCompiler,
                                   CCompiler cCompiler,
                                   CppCompiler cppCompiler,
                                   JsCompiler jsCompiler) {
        compilers.put(javaCompiler.getLanguage(), javaCompiler);
        compilers.put(pythonCompiler.getLanguage(), pythonCompiler);
        compilers.put(cCompiler.getLanguage(), cCompiler);
        compilers.put(cppCompiler.getLanguage(), cppCompiler);
        compilers.put(jsCompiler.getLanguage(), jsCompiler);
    }

    public LanguageCompiler getCompiler(String language) {
        LanguageCompiler compiler = compilers.get(language.toLowerCase());
        if (compiler == null) {
            throw new InvalidLanguageException("Unsupported language: " + language);
        }
        return compiler;
    }
}