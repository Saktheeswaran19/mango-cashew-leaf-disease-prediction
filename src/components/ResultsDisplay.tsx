import { AlertCircle, CheckCircle, Leaf } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface Disease {
  name: string;
  confidence: number;
  severity: "healthy" | "mild" | "moderate" | "severe";
  description: string;
  recommendations: string[];
}

interface ResultsDisplayProps {
  result: Disease | null;
}

export const ResultsDisplay = ({ result }: ResultsDisplayProps) => {
  if (!result) return null;

  const isHealthy = result.severity === "healthy";
  const severityColors = {
    healthy: "text-primary",
    mild: "text-yellow-600",
    moderate: "text-orange-600",
    severe: "text-destructive",
  };

  return (
    <Card className="shadow-medium border-border/50">
      <CardHeader>
        <div className="flex items-start gap-3">
          <div
            className={cn(
              "w-12 h-12 rounded-full flex items-center justify-center",
              isHealthy ? "bg-primary/10" : "bg-destructive/10"
            )}
          >
            {isHealthy ? (
              <CheckCircle className="w-6 h-6 text-primary" />
            ) : (
              <AlertCircle className="w-6 h-6 text-destructive" />
            )}
          </div>
          <div className="flex-1">
            <CardTitle className="text-2xl mb-1">{result.name}</CardTitle>
            <CardDescription className={cn("font-medium", severityColors[result.severity])}>
              {result.severity.charAt(0).toUpperCase() + result.severity.slice(1)}
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Confidence Level</span>
            <span className="text-sm font-bold">{Math.round(result.confidence * 100)}%</span>
          </div>
          <Progress value={result.confidence * 100} className="h-2" />
        </div>

        <div>
          <h4 className="text-sm font-semibold mb-2">Description</h4>
          <p className="text-sm text-muted-foreground">{result.description}</p>
        </div>

        {result.recommendations.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
              <Leaf className="w-4 h-4" />
              Recommendations
            </h4>
            <ul className="space-y-2">
              {result.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-muted-foreground">
                  <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
