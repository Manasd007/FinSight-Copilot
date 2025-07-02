import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { SidebarTrigger } from "@/components/ui/sidebar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Plus, User, Settings, LogOut, Moon, Sun, BarChart3, Menu } from "lucide-react";

interface HeaderProps {
  onNewChat: () => void;
}

export function Header({ onNewChat }: HeaderProps) {
  const [isDark, setIsDark] = useState(false);

  const toggleTheme = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle("dark");
  };

  return (
    <header className="h-16 bg-gradient-header border-b border-border flex items-center justify-between px-6 shadow-soft">
      {/* Sidebar Toggle and Logo */}
      <div className="flex items-center space-x-4">
        <SidebarTrigger>
          <Button
            variant="ghost"
            size="sm"
            className="text-primary-foreground/80 hover:text-primary-foreground hover:bg-primary-foreground/10 transition-all duration-300"
          >
            <Menu className="w-4 h-4" />
          </Button>
        </SidebarTrigger>
        
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-accent rounded-lg flex items-center justify-center shadow-medium animate-gentle-float">
            <BarChart3 className="w-5 h-5 text-accent-foreground" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-primary-foreground flex items-center">
              FinSight Copilot
              <Badge variant="secondary" className="ml-2 text-xs bg-accent/80 text-accent-foreground border-accent/30">
                AI
              </Badge>
            </h1>
          </div>
        </div>
      </div>

      {/* Center Actions */}
      <div className="flex items-center space-x-4">
        <Button
          onClick={onNewChat}
          variant="default"
          className="hover:bg-primary-dark transition-all duration-300"
        >
          <Plus className="w-4 h-4 mr-2" />
          New Chat
        </Button>
      </div>

      {/* Right Side Controls */}
      <div className="flex items-center space-x-4">
        {/* Theme Toggle */}
        <Button
          variant="ghost"
          size="sm"
          onClick={toggleTheme}
          className="text-primary-foreground/80 hover:text-primary-foreground hover:bg-primary-foreground/10 transition-all duration-300"
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </Button>

        {/* User Profile */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="relative h-10 w-10 rounded-full hover:bg-primary-foreground/10 transition-all duration-300">
              <Avatar className="h-10 w-10 border-2 border-primary-foreground/20">
                <AvatarImage src="/placeholder-avatar.jpg" alt="User" />
                <AvatarFallback className="bg-accent text-accent-foreground">
                  <User className="w-5 h-5" />
                </AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56 bg-popover border-border shadow-strong z-50" align="end" forceMount>
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium leading-none">Financial Analyst</p>
                <p className="text-xs leading-none text-muted-foreground">
                  analyst@finsight.com
                </p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="cursor-pointer hover:bg-accent/50 transition-all duration-200">
              <User className="mr-2 h-4 w-4" />
              <span>Profile</span>
            </DropdownMenuItem>
            <DropdownMenuItem className="cursor-pointer hover:bg-accent/50 transition-all duration-200">
              <Settings className="mr-2 h-4 w-4" />
              <span>Settings</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="cursor-pointer text-destructive hover:bg-destructive/20 transition-all duration-200">
              <LogOut className="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}