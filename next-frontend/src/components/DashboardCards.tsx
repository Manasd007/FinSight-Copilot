import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, DollarSign, BarChart3, Users, Calendar } from "lucide-react";

export function DashboardCards() {
  const marketData = [
    {
      title: "S&P 500",
      value: "4,783.45",
      change: "+1.2%",
      trend: "up",
      icon: TrendingUp
    },
    {
      title: "NASDAQ",
      value: "15,012.33",
      change: "+0.8%",
      trend: "up",
      icon: BarChart3
    },
    {
      title: "Portfolio Value",
      value: "$2.4M",
      change: "+5.7%",
      trend: "up",
      icon: DollarSign
    },
    {
      title: "Active Positions",
      value: "23",
      change: "+2",
      trend: "up",
      icon: Users
    }
  ];

  const recentAnalyses = [
    {
      company: "AAPL",
      title: "Q4 Earnings Analysis",
      type: "Earnings Call",
      timestamp: "2 hours ago",
      sentiment: "Bullish"
    },
    {
      company: "TSLA",
      title: "Production Update Review",
      type: "10-Q",
      timestamp: "5 hours ago",
      sentiment: "Neutral"
    },
    {
      company: "MSFT",
      title: "Azure Growth Assessment",
      type: "10-K",
      timestamp: "1 day ago",
      sentiment: "Bullish"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Market Overview */}
      <div>
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-primary" />
          Market Overview
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {marketData.map((item) => (
            <Card key={item.title} className="shadow-soft hover:shadow-medium transition-shadow duration-200">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {item.title}
                </CardTitle>
                <item.icon className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">{item.value}</div>
                <div className="flex items-center space-x-1 mt-1">
                  {item.trend === "up" ? (
                    <TrendingUp className="h-3 w-3 text-success" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-destructive" />
                  )}
                  <span className={`text-xs font-medium ${
                    item.trend === "up" ? "text-success" : "text-destructive"
                  }`}>
                    {item.change}
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Recent Analyses */}
      <div>
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center">
          <Calendar className="w-5 h-5 mr-2 text-primary" />
          Recent Analyses
        </h3>
        <Card className="shadow-soft">
          <CardContent className="p-0">
            <div className="divide-y divide-border">
              {recentAnalyses.map((analysis, index) => (
                <div key={index} className="p-4 hover:bg-muted/50 transition-colors duration-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center">
                        <span className="text-sm font-bold text-primary-foreground">
                          {analysis.company}
                        </span>
                      </div>
                      <div>
                        <h4 className="text-sm font-medium text-foreground">
                          {analysis.title}
                        </h4>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge variant="secondary" className="text-xs">
                            {analysis.type}
                          </Badge>
                          <span className="text-xs text-muted-foreground">
                            {analysis.timestamp}
                          </span>
                        </div>
                      </div>
                    </div>
                    <Badge 
                      variant={analysis.sentiment === "Bullish" ? "default" : "secondary"}
                      className={
                        analysis.sentiment === "Bullish" 
                          ? "bg-success text-success-foreground" 
                          : ""
                      }
                    >
                      {analysis.sentiment}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}