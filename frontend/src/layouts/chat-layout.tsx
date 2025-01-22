import { AppSidebar } from "@/components/app-sidebar";
import { ModeToggle } from "@/components/ModeToggle";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Outlet } from "react-router";

function ChatLayout() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-14 items-center gap-4 border-b bg-background px-6 lg:h-[60px]">
          <SidebarTrigger className="dark:text-black" />
          <Separator orientation="vertical" className="h-6" />
          <div className="flex flex-1 justify-between">
            <span className="text-lg font-semibold">MedicalChatBot</span>
            <span className="flex gap-2">
              <ModeToggle />
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
export default ChatLayout;
