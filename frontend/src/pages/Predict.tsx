import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Upload, ArrowLeft, ImageIcon, Loader2 } from "lucide-react";

const API_BASE = "/api";

const Predict = () => {
  const navigate = useNavigate();
  const fileRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFile = (f: File) => {
    setFile(f);
    setResult(null);
    setError(null);

    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target?.result as string);
    reader.readAsDataURL(f);
  };

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/upload/`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const detail = await res.json().catch(() => null);
        throw new Error(detail?.detail || "Prediction failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="mx-auto max-w-2xl px-6 py-16">
        <button
          onClick={() => navigate("/")}
          className="mb-10 inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          Back
        </button>

        <h1 className="mb-2 text-3xl font-bold text-foreground">
          Classify image
        </h1>

        <p className="mb-10 text-muted-foreground">
          Upload a skin tumor image and the model will classify it.
        </p>

        {/* Upload zone */}
        <div
          onClick={() => fileRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            const f = e.dataTransfer.files[0];
            if (f) handleFile(f);
          }}
          className="group flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-border bg-card p-12 text-center hover:border-primary/40 hover:bg-secondary/50"
        >
          {preview ? (
            <img
              src={preview}
              alt="Preview"
              className="mb-4 max-h-64 rounded-lg object-contain"
            />
          ) : (
            <ImageIcon className="mb-4 h-12 w-12 text-muted-foreground/50" />
          )}

          <p className="text-sm font-medium text-muted-foreground">
            {file ? file.name : "Click or drag & drop an image"}
          </p>

          <input
            ref={fileRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) handleFile(f);
            }}
          />
        </div>

        <Button
          className="mt-6 w-full gap-2"
          size="lg"
          disabled={!file || loading}
          onClick={handleSubmit}
        >
          {loading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Upload className="h-4 w-4" />
          )}
          {loading ? "Classifying…" : "Upload & Classify"}
        </Button>

        {/* ✅ RESULTADO BONITO (SIN JSON) */}
        {result && (
          <div
            className="mt-8 rounded-xl border border-border bg-card p-6 text-center"
            style={{
              backgroundColor:
                result.predicted_class === "malignant"
                  ? "rgba(255, 0, 0, 0.06)"
                  : "rgba(0, 200, 0, 0.06)",
            }}
          >
            <h3 className="mb-4 text-lg font-semibold">
              Prediction Result
            </h3>

            <p className="text-xl">
              The predicted class is{" "}
              <span className="text-2xl font-bold">
                {result.predicted_class.toUpperCase()}
              </span>
            </p>

            <p className="mt-2 text-lg text-muted-foreground">
              with a confidence of{" "}
              <span className="font-semibold text-foreground">
                {Math.round(result.confidence * 100)}%
              </span>
            </p>
          </div>
        )}

        {error && (
          <div className="mt-6 rounded-lg border border-destructive/30 bg-destructive/10 p-4 text-sm text-destructive">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default Predict;