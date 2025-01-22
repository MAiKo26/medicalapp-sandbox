import useStore from "@/app/store/usernamestore";
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
import { BotMessageSquare, Calendar, MessageCircleMore } from "lucide-react";
import { Link } from "react-router";
import { Button } from "./ui/button";
import { useState } from "react";

const navigation = [
  { name: "General Chat", href: "/chat/general", icon: MessageCircleMore },
  { name: "Bot Chat", href: "/chat/bot", icon: BotMessageSquare },
];

export function AppSidebar() {
  const { username, setUsername } = useStore();
  const [newUsername, setNewUsername] = useState(username);
  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center gap-2 px-4 py-2">
          <Calendar className="h-6 w-6" />
          <span className="font-semibold">MedicalChatBot</span>
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
        <div className="flex h-20 flex-col items-start justify-center gap-1 border-t p-2">
          <p className="font-bold">Change Your Username here : </p>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Change username"
              className="w-2/3 rounded border px-2 py-1 text-sm"
              onChange={(e) => setNewUsername(e.target.value)}
              value={newUsername}
            />
            <Button className="1/3" onClick={() => setUsername(newUsername)}>
              Save
            </Button>
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
