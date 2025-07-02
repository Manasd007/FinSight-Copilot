import { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  History,
  Upload,
  Settings,
  HelpCircle,
  LogOut,
  Cog,
  BarChart3,
  Key,
  Zap
} from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

const menuItems = [
  { title: "Dashboard", url: "/", icon: LayoutDashboard },
  { title: "Chat History", url: "/history", icon: History },
  { title: "Upload Document", url: "/upload", icon: Upload },
  { title: "Export Chat", url: "/export", icon: LogOut },
  { title: "Settings", url: "/settings", icon: Settings },
  { title: "Help & Support", url: "/help", icon: HelpCircle },
  { title: "Integrations", url: "/integrations", icon: Zap },
  { title: "API Keys", url: "/api-keys", icon: Key },
  { title: "Analytics", url: "/analytics", icon: BarChart3 },
];

const companies = ["Apple", "Tesla", "Microsoft", "Google", "Amazon"];
const documentTypes = ["10-K", "10-Q", "Earnings Calls"];

export function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const location = useLocation();
  const currentPath = location.pathname;
  const [selectedCompany, setSelectedCompany] = useState("");
  const [selectedDocs, setSelectedDocs] = useState<string[]>([]);

  const isActive = (path: string) => currentPath === path;

  const handleDocumentToggle = (doc: string) => {
    setSelectedDocs(prev => 
      prev.includes(doc) 
        ? prev.filter(d => d !== doc)
        : [...prev, doc]
    );
  };

  return (
    <Sidebar className="bg-gradient-sidebar border-r border-sidebar-border transition-all duration-300 ease-in-out" collapsible="icon">
      <SidebarContent className="p-4 space-y-6">
        {/* Logo Section */}
        <div className={`transition-all duration-300 ease-in-out ${collapsed ? 'opacity-80' : 'opacity-100'}`}>
          <div className="flex items-center space-x-3 p-2">
            <div className="w-8 h-8 bg-gradient-accent rounded-lg flex items-center justify-center shadow-soft animate-subtle-fade">
              <BarChart3 className="w-5 h-5 text-accent-foreground" />
            </div>
            {!collapsed && (
              <div>
                <h2 className="text-lg font-semibold text-sidebar-foreground">FinSight</h2>
                <p className="text-sm text-sidebar-foreground/70">Copilot</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <SidebarGroup>
          <SidebarGroupLabel className="text-sidebar-foreground/70 uppercase tracking-wider text-xs font-medium mb-2">
            Navigation
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu className="space-y-1">
              {menuItems.map((item) => (
                <SidebarMenuItem key={item.title} className="transition-all duration-200 hover:translate-x-1">
                  <NavLink
                    to={item.url}
                    className={`flex items-center px-3 py-2 rounded-lg transition-all duration-200 ${
                      isActive(item.url)
                        ? "bg-primary text-primary-foreground font-medium shadow-soft"
                        : "text-sidebar-foreground/80 hover:bg-sidebar-accent hover:text-sidebar-foreground"
                    }`}
                  >
                    <item.icon className={`${collapsed ? "w-5 h-5" : "w-4 h-4 mr-3"} transition-all duration-200`} />
                    {!collapsed && <span className="text-sm">{item.title}</span>}
                  </NavLink>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        {/* Filters Section */}
        {!collapsed && (
          <Card className="p-4 bg-card border-sidebar-border shadow-soft">
            <div className="space-y-4">
              <div>
                <Label className="text-sm font-medium text-sidebar-foreground mb-2 block">
                  Company Selector
                </Label>
                <Select value={selectedCompany} onValueChange={setSelectedCompany}>
                  <SelectTrigger className="w-full bg-sidebar-accent border-sidebar-border text-sidebar-foreground">
                    <SelectValue placeholder="Select a company" />
                  </SelectTrigger>
                  <SelectContent className="bg-popover border-border z-50">
                    {companies.map((company) => (
                      <SelectItem key={company} value={company.toLowerCase()}>
                        {company}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label className="text-sm font-medium text-sidebar-foreground mb-2 block">
                  Document Filters
                </Label>
                <div className="space-y-2">
                  {documentTypes.map((doc) => (
                    <div key={doc} className="flex items-center space-x-2">
                      <Checkbox
                        id={doc}
                        checked={selectedDocs.includes(doc)}
                        onCheckedChange={() => handleDocumentToggle(doc)}
                        className="border-sidebar-border data-[state=checked]:bg-primary data-[state=checked]:border-primary"
                      />
                      <Label
                        htmlFor={doc}
                        className="text-sm text-sidebar-foreground/80 cursor-pointer"
                      >
                        {doc}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Card>
        )}

      </SidebarContent>
    </Sidebar>
  );
}