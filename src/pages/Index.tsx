import { useState } from "react";
import { Leaf, Shield, Zap } from "lucide-react";
import { ImageUpload } from "@/components/ImageUpload";
import { ResultsDisplay } from "@/components/ResultsDisplay";
import { Button } from "@/components/ui/button";
import { toast } from "@/hooks/use-toast";

const Index = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleImageSelect = (file: File) => {
    setSelectedFile(file);
    setResult(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    
    // Simulate API call - replace with your actual backend endpoint
    try {
       const formData = new FormData();
       formData.append('image', selectedFile);
       
       const response = await fetch("http://localhost:8000/api/analyze", {
         method: 'POST',
         body: formData,
       });
       
       const data = await response.json();
      
      // Mock response for demo
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const mockResult = {
        name: "Anthracnose",
        confidence: 0.89,
        severity: "moderate" as const,
        description: "Anthracnose is a fungal disease that causes dark lesions on leaves and fruit. It typically appears during warm, humid weather conditions.",
        recommendations: [
          "Remove and destroy infected leaves immediately",
          "Apply copper-based fungicide every 10-14 days",
          "Improve air circulation around trees",
          "Avoid overhead watering to reduce leaf wetness",
          "Consider using resistant mango varieties for future planting"
        ]
      };
      
      setResult(mockResult);
      toast({
        title: "Analysis Complete",
        description: "Your mango leaf has been analyzed successfully.",
      });
    } catch (error) {
      toast({
        title: "Analysis Failed",
        description: "There was an error analyzing your image. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen gradient-subtle">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,hsl(145_45%_35%/0.1),transparent_50%)]" />
        <div className="container mx-auto px-4 py-16 relative">
          <div className="max-w-4xl mx-auto text-center mb-12">
            <div className="inline-flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-full mb-6">
              <Leaf className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium text-primary">AI-Powered Detection</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Mango Leaf Disease Detector
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Protect your mango trees with instant AI-powered disease detection. 
              Upload a photo and get accurate results in seconds.
            </p>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-12">
            <div className="bg-card rounded-xl p-6 shadow-soft border border-border/50">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">Instant Results</h3>
              <p className="text-sm text-muted-foreground">
                Get disease detection results in just a few seconds
              </p>
            </div>
            <div className="bg-card rounded-xl p-6 shadow-soft border border-border/50">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">High Accuracy</h3>
              <p className="text-sm text-muted-foreground">
                Trained on thousands of mango leaf images
              </p>
            </div>
            <div className="bg-card rounded-xl p-6 shadow-soft border border-border/50">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Leaf className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">Expert Advice</h3>
              <p className="text-sm text-muted-foreground">
                Receive treatment recommendations for detected diseases
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Upload Section */}
      <section className="container mx-auto px-4 pb-16">
        <div className="max-w-3xl mx-auto space-y-8">
          <div className="bg-card rounded-2xl p-8 shadow-medium border border-border/50">
            <h2 className="text-2xl font-bold mb-6">Upload Mango Leaf Image</h2>
            <ImageUpload onImageSelect={handleImageSelect} isAnalyzing={isAnalyzing} />
            {selectedFile && !result && (
              <div className="mt-6 flex justify-center">
                <Button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
                  size="lg"
                  className="gradient-primary text-white font-semibold px-8"
                >
                  {isAnalyzing ? "Analyzing..." : "Analyze Image"}
                </Button>
              </div>
            )}
          </div>

          {result && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
              <ResultsDisplay result={result} />
              <div className="mt-6 flex justify-center">
                <Button
                  onClick={() => {
                    setSelectedFile(null);
                    setResult(null);
                  }}
                  variant="outline"
                  size="lg"
                >
                  Analyze Another Image
                </Button>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 mt-16">
        <div className="container mx-auto px-4 py-8">
          <p className="text-center text-sm text-muted-foreground">
            © 2024 Mango Leaf Disease Detector. Protecting your harvest with AI.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
