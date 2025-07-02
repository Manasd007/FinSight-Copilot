import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Send, Bot, User, Loader2, BarChart3, TrendingUp, DollarSign } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: string;
  content: string;
  sender: "user" | "bot";
  timestamp: Date;
  isTyping?: boolean;
}

interface ChatInterfaceProps {
  onNewMessage?: (message: Message) => void;
}

const promptTypes = ["RAG", "Advice", "Summary", "Analysis", "Forecast"];
const responseStyles = ["Structured", "Narrative"];

export function ChatInterface({ onNewMessage }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [promptType, setPromptType] = useState("RAG");
  const [responseStyle, setResponseStyle] = useState("Structured");
  const [isTyping, setIsTyping] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const simulateTyping = async (text: string): Promise<void> => {
    return new Promise((resolve) => {
      let index = 0;
      const botMessageId = Date.now().toString();
      
      const typeMessage: Message = {
        id: botMessageId,
        content: "",
        sender: "bot",
        timestamp: new Date(),
        isTyping: true
      };
      
      setMessages(prev => [...prev, typeMessage]);
      setIsTyping(true);

      const interval = setInterval(() => {
        if (index < text.length) {
          setMessages(prev => 
            prev.map(msg => 
              msg.id === botMessageId 
                ? { ...msg, content: text.slice(0, index + 1) }
                : msg
            )
          );
          index++;
        } else {
          clearInterval(interval);
          setMessages(prev => 
            prev.map(msg => 
              msg.id === botMessageId 
                ? { ...msg, isTyping: false }
                : msg
            )
          );
          setIsTyping(false);
          resolve();
        }
      }, 30);
    });
  };

  const generateResponse = (userMessage: string): string => {
    const responses = {
      "RAG": `Based on the latest financial documents, here's what I found:\n\n📊 **Key Metrics:**\n• Revenue: $394.3B (+2.8% YoY)\n• Net Income: $99.8B (+5.4% YoY)\n• EPS: $6.16 (+5.6% YoY)\n\n💡 **Analysis:** The company shows strong fundamentals with consistent growth across key metrics. The latest 10-K filing indicates robust cash flow and healthy margins.`,
      "Advice": `💼 **Investment Recommendation:**\n\nBased on current market conditions and financial analysis:\n\n🟢 **BUY** - Strong fundamentals support long-term growth\n• P/E ratio attractive at current levels\n• Strong competitive moat in technology sector\n• Consistent dividend payments\n\n⚠️ **Risk Factors:** Market volatility, regulatory changes`,
      "Summary": `📋 **Executive Summary:**\n\nCompany performance highlights:\n• Strong revenue growth trajectory\n• Improved operational efficiency\n• Solid balance sheet position\n• Positive market sentiment\n\nRecommend monitoring upcoming earnings call for guidance updates.`,
      "Analysis": `🔍 **Deep Financial Analysis:**\n\n**Profitability Metrics:**\n• Gross Margin: 43.8% (+120bps YoY)\n• Operating Margin: 25.3% (+85bps YoY)\n• ROE: 22.4% (industry avg: 18.2%)\n\n**Liquidity & Solvency:**\n• Current Ratio: 1.8x (healthy)\n• Debt-to-Equity: 0.31x (conservative)\n• Free Cash Flow: $84.2B (+12% YoY)`,
      "Forecast": `🔮 **Financial Forecast:**\n\n**Next Quarter Projections:**\n• Revenue: $98-102B (est.)\n• EPS: $1.45-1.55 (est.)\n• Margin expansion expected\n\n**FY2024 Outlook:**\n• Revenue growth: 8-12%\n• Continued market share gains\n• AI investments driving innovation`
    };

    return responses[promptType as keyof typeof responses] || 
           "I'd be happy to help you analyze financial data. Please provide more specific details about what you'd like to explore.";
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    // Simulate API delay
    setTimeout(async () => {
      const response = generateResponse(inputValue);
      await simulateTyping(response);
      setIsLoading(false);
      
      toast({
        title: "Analysis Complete",
        description: "Financial insights have been generated.",
      });
      
      if (onNewMessage) {
        onNewMessage(userMessage);
      }
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-background">
      {/* Chat Controls */}
      <div className="p-4 border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="flex gap-4 items-center">
          <div className="flex-1">
            <label className="text-sm font-medium text-foreground mb-1 block">Prompt Type</label>
            <Select value={promptType} onValueChange={setPromptType}>
              <SelectTrigger className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {promptTypes.map(type => (
                  <SelectItem key={type} value={type}>{type}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex-1">
            <label className="text-sm font-medium text-foreground mb-1 block">Response Style</label>
            <Select value={responseStyle} onValueChange={setResponseStyle}>
              <SelectTrigger className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {responseStyles.map(style => (
                  <SelectItem key={style} value={style}>{style}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
        <div className="space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gradient-primary rounded-full flex items-center justify-center mx-auto mb-4 shadow-medium">
                <BarChart3 className="w-8 h-8 text-primary-foreground" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">Welcome to FinSight Copilot</h3>
              <p className="text-muted-foreground max-w-md mx-auto">
                Ask me anything about financial data or markets...
              </p>
              <div className="flex justify-center gap-2 mt-4">
                <Badge variant="outline" className="text-xs">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  Market Analysis
                </Badge>
                <Badge variant="outline" className="text-xs">
                  <DollarSign className="w-3 h-3 mr-1" />
                  Investment Advice
                </Badge>
                <Badge variant="outline" className="text-xs">
                  <BarChart3 className="w-3 h-3 mr-1" />
                  Financial Reports
                </Badge>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"} animate-fade-in`}
            >
              <div className={`flex max-w-[70%] ${message.sender === "user" ? "flex-row-reverse" : "flex-row"} gap-3`}>
                <Avatar className="w-8 h-8 mt-1">
                  <AvatarFallback className={message.sender === "user" ? "bg-chat-user text-chat-user-foreground" : "bg-chat-bot text-chat-bot-foreground"}>
                    {message.sender === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                  </AvatarFallback>
                </Avatar>
                
                <Card className={`p-3 ${
                  message.sender === "user" 
                    ? "bg-chat-user text-chat-user-foreground" 
                    : "bg-chat-bot text-chat-bot-foreground border-border"
                } shadow-soft`}>
                  <div className="text-sm whitespace-pre-line">
                    {message.content}
                    {message.isTyping && (
                      <span className="inline-block w-2 h-5 bg-current animate-pulse-slow ml-1" />
                    )}
                  </div>
                  <div className="text-xs opacity-70 mt-1">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </Card>
              </div>
            </div>
          ))}

          {isLoading && !isTyping && (
            <div className="flex justify-start animate-fade-in">
              <div className="flex gap-3 max-w-[70%]">
                <Avatar className="w-8 h-8 mt-1">
                  <AvatarFallback className="bg-chat-bot text-chat-bot-foreground">
                    <Bot className="w-4 h-4" />
                  </AvatarFallback>
                </Avatar>
                <Card className="p-3 bg-chat-bot text-chat-bot-foreground border-border shadow-soft">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">Analyzing financial data...</span>
                  </div>
                </Card>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input Area */}
      <div className="p-4 border-t border-border bg-card/50 backdrop-blur-sm">
        <div className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about company performance, stock trends, or investment strategies..."
            className="flex-1"
            disabled={isLoading}
          />
          <Button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="bg-primary hover:bg-primary-dark text-primary-foreground shadow-medium"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}