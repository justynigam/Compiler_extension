import Editor from '@monaco-editor/react';

interface CodeEditorProps {
  language: string;
  code: string;
  onChange: (value: string | undefined) => void;
  theme?: string;
}

const languageMap: Record<string, string> = {
  java: 'java',
  python: 'python',
  c: 'c',
  cpp: 'cpp',
  javascript: 'javascript',
};

const CodeEditor: React.FC<CodeEditorProps> = ({
  language,
  code,
  onChange,
  theme = 'vs-dark',
}) => {
  return (
    <div className="flex-1 h-full w-full">
      <Editor
        height="100%"
        language={languageMap[language] || 'plaintext'}
        value={code}
        onChange={onChange}
        theme={theme}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          wordWrap: 'on',
        }}
      />
    </div>
  );
};

export default CodeEditor;