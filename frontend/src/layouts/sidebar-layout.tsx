import { Outlet } from "react-router";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/sidebar-app";
import { Separator } from "@/components/ui/separator";
import { LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { logout } from "@/lib/logout";
import { ModeToggle } from "@/components/mode-toggle";

function SidebarLayout() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
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
        <div className="w-full flex-1 overflow-y-auto overflow-x-hidden bg-background p-5">
          <Outlet />
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
export default SidebarLayout;
