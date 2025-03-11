import { Outlet, useNavigate } from "react-router";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/sidebar-app";
import { Separator } from "@/components/ui/separator";
import { LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ModeToggle } from "@/components/mode-toggle";
import { env } from "@/config/env";

import { toast } from "@/hooks/use-toast";

function SidebarLayout() {
  const navigate = useNavigate();
  async function logout() {
    try {
      const response = await fetch(`${env.VITE_API_URL}/auth/logout`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        toast({
          title: "Logout failed",
          description: "Server down.",
          variant: "destructive",
        });
        return;
      }

      toast({
        title: "Logout successful",
        description: "Comeback soon!",
      });

      navigate("/auth/login");
    } catch (error) {
      console.error("Login error:", error);
    }
  }
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset className="max-h-lvh overflow-hidden">
        <header className="flex h-14 items-center gap-4 border-b bg-background px-6 lg:h-[60px]">
          <SidebarTrigger className="bg-background" />
          <Separator orientation="vertical" className="h-6" />
          <div className="flex flex-1 justify-end">
            <span className="flex gap-2">
              <ModeToggle />
              <Button onClick={() => logout()}>
                <LogOut />
              </Button>
            </span>
          </div>
        </header>
        <div className="h-full w-full flex-1 overflow-x-hidden bg-background p-5">
          <Outlet />
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
export default SidebarLayout;
