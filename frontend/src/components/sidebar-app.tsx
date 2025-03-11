import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { env } from "@/config/env";

import { User } from "@/interfaces/user-interface";
import {
  BotMessageSquare,
  BrainCircuitIcon,
  Home,
  MessageCircleMore,
  Settings,
} from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import { NavUser } from "./sidebar-user";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: Home },
  {
    name: "General Chat",
    href: "/dashboard/chat/general",
    icon: MessageCircleMore,
  },
  { name: "Bot Chat", href: "/dashboard/chat/bot", icon: BotMessageSquare },
  { name: "AI Chat", href: "/dashboard/chat/ai", icon: BrainCircuitIcon },
  { name: "Settings", href: "/dashboard/settings", icon: Settings },
];

export function AppSidebar() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`${env.VITE_API_URL}/auth/me`, {
          method: "GET",
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to fetch user");
        }

        const user: User = await response.json();
        setCurrentUser(user);

        if (!user) {
          window.location.href = "/auth/login";
        }
      } catch (error) {
        console.error("Error fetching user:", error);
        window.location.href = "/auth/login";
      }
    };

    fetchUser();
  }, []);
  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center gap-2 px-4 py-2">
          <img src="/favicon.svg" className="h-6 w-6" />
          <span className="font-semibold">MedicalApp SandBox</span>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigation.map((item) => (
                <SidebarMenuItem key={item.name}>
                  <SidebarMenuButton asChild>
                    <Link to={item.href}>
                      <item.icon className="h-4 w-4" />
                      <span>{item.name}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <NavUser {...currentUser} />
      </SidebarFooter>
    </Sidebar>
  );
}
