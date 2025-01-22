import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import { NotFound } from "./app/not-found";
import { ThemeProvider } from "./components/theme-provider";
import { Toaster } from "./components/ui/toaster";
import ChatLayout from "./layouts/chat-layout";
import Chat from "./app/chat/chat";
import BotChat from "./app/chat/BotChat";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/chat/bot" />} />
          <Route path="chat" element={<ChatLayout />}>
            <Route path="general" element={<Chat />} />
            <Route path="bot" element={<BotChat />} />
          </Route>

          <Route path="*" element={<NotFound />} />
        </Routes>
        <Toaster />
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
