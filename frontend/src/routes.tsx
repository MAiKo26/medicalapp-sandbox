import LoginPage from "@/app/(auth)/auth/login";
import RegisterPage from "@/app/(auth)/auth/register";
import BotChat from "@/app/(dashboard)/chat/BotChat";
import Chat from "@/app/(dashboard)/chat/chat";
import AdminPage from "@/app/(dashboard)/dashboard/admin/admin";
import { NotFound } from "@/app/not-found";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/ui/toaster";
import AuthLayout from "@/layouts/auth-layout";
import SidebarLayout from "@/layouts/sidebar-layout";
import { BrowserRouter, Route, Routes } from "react-router";
import AiChat from "./app/(dashboard)/chat/ai-chat";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <Routes>
          <Route path="dashboard" element={<SidebarLayout />}>
            <Route index element={<AdminPage />} />
            <Route path="chat">
              <Route path="general" element={<Chat />} />
              <Route path="bot" element={<BotChat />} />
              <Route path="ai" element={<AiChat />} />
            </Route>
            <Route path="*" element={<NotFound />} />
          </Route>
          <Route path="auth" element={<AuthLayout />}>
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Toaster />
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
