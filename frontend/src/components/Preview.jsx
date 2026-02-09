import { useState } from "react";

export default function PreviewPage({ generatedFiles }) {
  const [selectedFile, setSelectedFile] = useState(null);

  // Detect project type
  const isBackendProject =
    generatedFiles?.["main.py"] ||
    generatedFiles?.["models.py"] ||
    generatedFiles?.["schemas.py"] ||
    generatedFiles?.["requirements.txt"];

  const appFile =
    generatedFiles?.["App.jsx"] ||
    generatedFiles?.["app.jsx"] ||
    generatedFiles?.["App.js"] ||
    generatedFiles?.["app.js"];

  const isFrontendProject = !!appFile;

  // Detect simple HTML (no imports/JSX)
  const htmlFiles = Object.keys(generatedFiles || {}).filter((f) =>
    f.endsWith(".html")
  );

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert("Copied to clipboard!");
    });
  };

  return (
    <div className="flex h-[70vh] border rounded-lg overflow-hidden">

      {/* ================= FILE LIST ================= */}
      <div className="w-64 border-r p-4 bg-slate-50 overflow-auto">
        <h3 className="font-semibold mb-3">Generated Files</h3>

        {Object.keys(generatedFiles || {}).map((file) => (
          <div
            key={file}
            onClick={() => setSelectedFile(file)}
            className={`text-sm cursor-pointer mb-1 ${
              selectedFile === file
                ? "text-indigo-600 font-medium"
                : "hover:text-indigo-600"
            }`}
          >
            📄 {file}
          </div>
        ))}
      </div>

      {/* ================= CODE VIEWER ================= */}
      <div className="flex-1 bg-slate-900 text-slate-100 p-4 overflow-auto text-sm">
        {selectedFile ? (
          <pre className="whitespace-pre-wrap">
            <code>{generatedFiles[selectedFile]}</code>
          </pre>
        ) : (
          <div className="text-slate-400">Select a file to view its code</div>
        )}
      </div>

      {/* ================= PREVIEW PANEL ================= */}
      <div className="w-1/3 border-l bg-white p-4 overflow-auto space-y-4">

        {/* 🟡 Backend Project */}
        {isBackendProject && !isFrontendProject && (
          <div className="text-center">
            <h3 className="font-semibold text-lg mb-2">Backend Project Detected</h3>
            <p className="text-sm text-gray-600 mb-4">
              Live preview is not supported for backend-only projects.
            </p>

            <div className="text-left bg-gray-100 p-4 rounded text-sm space-y-2">
              <p className="font-medium mb-1">Run locally:</p>
              <pre className="bg-black text-green-400 p-2 rounded text-xs">
docker-compose up --build
              </pre>
              <button
                onClick={() => copyToClipboard("docker-compose up --build")}
                className="px-3 py-1 bg-indigo-600 text-white rounded text-xs hover:bg-indigo-700"
              >
                Copy & Run Locally
              </button>
              <p className="mt-2 text-xs text-gray-600">
                Then open: <strong>http://localhost:8000</strong>
              </p>
            </div>
          </div>
        )}

        {/* 🟢 Frontend React/Vite Project */}
        {isFrontendProject && (
          <div className="text-center">
            <h3 className="font-semibold text-lg mb-2">Frontend Project Detected</h3>
            <p className="text-sm text-gray-600 mb-2">
              Live preview of complex React apps is not supported in-browser.
            </p>

            <div className="text-left bg-gray-100 p-4 rounded text-sm space-y-2">
              <p className="font-medium">Run locally:</p>
              <pre className="bg-black text-green-400 p-2 rounded text-xs">
npm install && npm start
              </pre>
              <div className="flex gap-2 mt-1">
                <button
                  onClick={() => copyToClipboard("npm install && npm start")}
                  className="px-3 py-1 bg-indigo-600 text-white rounded text-xs hover:bg-indigo-700"
                >
                  Copy & Run Locally
                </button>
                
                <a
                  href="https://codesandbox.io/s/new"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-3 py-1 bg-yellow-500 text-white rounded text-xs hover:bg-yellow-600"
                >
                  Open in CodeSandbox
                </a>
              </div>
            </div>
          </div>
        )}

        {/* ⚪ Simple HTML/CSS files */}
        {htmlFiles.length > 0 && htmlFiles.map((file) => (
          <div key={file} className="space-y-2">
            <h3 className="font-semibold text-gray-700 text-sm mb-1">{file} Preview</h3>
            <iframe
              title={`Preview - ${file}`}
              srcDoc={generatedFiles[file]}
              className="w-full h-48 border"
            />
          </div>
        ))}

        {/* 🔹 Fallback */}
        {!isBackendProject && !isFrontendProject && htmlFiles.length === 0 && (
          <div className="text-center text-gray-500">
            No preview available.
          </div>
        )}
      </div>
    </div>
  );
}
