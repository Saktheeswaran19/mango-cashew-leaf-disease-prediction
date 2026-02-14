import { AlertCircle, CheckCircle, Leaf } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

interface Disease {
  name?: string | null;
  confidence?: number | null; // already in %
  severity?: "healthy" | "mild" | "moderate" | "severe" | null;
  description?: string | null;
  recommendations?: string[] | null;
  all_probabilities?: Record<string, number> | null;
}


interface ResultsDisplayProps {
  result: Disease | null;
}

export const ResultsDisplay = ({ result }: ResultsDisplayProps) => {
  if (!result) return null;

  // Defensive fallbacks
  const name = result.name ?? "Unknown";
  const confidence = typeof result.confidence === "number" ? result.confidence : parseFloat(String(result.confidence ?? "0")) || 0;
  const severity = result.severity ?? null; // keep null if not provided
  const description = result.description ?? null;
  const recommendations = Array.isArray(result.recommendations) ? result.recommendations : [];
  const chartData =
    result.all_probabilities
      ? Object.entries(result.all_probabilities).map(([name, value]) => ({
        name,
        probability: value,
      }))
      : [];
  const isHealthy = severity === "healthy";

  const severityColors: Record<string, string> = {
    healthy: "text-primary",
    mild: "text-yellow-600",
    moderate: "text-orange-600",
    severe: "text-destructive",
    unknown: "text-muted-foreground",
  };

  // Safe helper - returns first letter or "?" if not available
  const firstLetter = (s?: string | null) => (s && typeof s === "string" && s.length > 0 ? s.charAt(0).toUpperCase() : "?");

  // Safe display of severity text (capitalized) or fallback
  const severityLabel = severity && typeof severity === "string"
    ? severity.charAt(0).toUpperCase() + severity.slice(1)
    : "Unknown";

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
            <CardTitle className="text-2xl mb-1">{name}</CardTitle>
            <CardDescription
              className={cn(
                "font-medium",
                severity
                  ? severityColors[severity] ?? severityColors["unknown"]
                  : severityColors["unknown"]
              )}
            >
              {severityLabel}
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Confidence Section */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Confidence Level</span>
            <span className="text-sm font-bold">
              {confidence.toFixed(2)}%
            </span>
          </div>

          <Progress
            value={Math.min(Math.max(confidence, 0), 100)}
            className="h-2"
          />
        </div>

        {/* Probability Distribution Bar Chart */}
        {chartData.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-3">
              Probability Distribution Across Diseases
            </h4>

            <div className="w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="name"
                    tick={{ fontSize: 10 }}
                    interval={0}
                    angle={-20}
                    textAnchor="end"
                  />
                  <YAxis domain={[0, 100]} />
                  <Tooltip
                    formatter={(value: number) =>
                      `${value.toFixed(2)}%`
                    }
                  />
                  <Bar
                    dataKey="probability"
                    radius={[6, 6, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Description */}
        <div>
          <h4 className="text-sm font-semibold mb-2">Description</h4>
          <p className="text-sm text-muted-foreground">
            {description ?? "No description available."}
          </p>
        </div>

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
              <Leaf className="w-4 h-4" />
              Recommendations
            </h4>

            <ul className="space-y-2">
              {recommendations.map((rec, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-sm text-muted-foreground"
                >
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
