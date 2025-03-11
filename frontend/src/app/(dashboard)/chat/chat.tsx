import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send } from "lucide-react";
import { useEffect, useState } from "react";
import useStore from "@/config/app-store";
import { toast } from "@/hooks/use-toast";
import { env } from "@/config/env";

interface Message {
  sender: string;
  content: string;
}

export default function Chat() {
  const { username } = useStore();
  const [messageInput, setMessageInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSending, setIsSending] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(
      `${env.VITE_API_URL.replace("http", "ws")}/ws/chat/general/${username}`,
    );

    socket.onopen = () => {
      console.log("WebSocket connection opened");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, data]);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, [username]);

  const handleSend = async () => {
    if (!messageInput.trim() || isSending || !ws) return;

    try {
      setIsSending(true);

      ws.send(messageInput);
      setMessageInput("");
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to send message.",
        variant: "destructive",
      });
      console.error("Failed to send message:", error);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <Card className="h-[calc(100vh-2rem)]">
      <CardHeader>
        <CardTitle>General Chat</CardTitle>
      </CardHeader>
      <CardContent className="flex h-[calc(100%-8rem)] flex-col gap-4">
        <ScrollArea className="flex-1 rounded-lg border p-4">
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex items-start gap-4 ${
                  message.sender === username ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`grid gap-1 rounded-lg p-3 ${
                    message.sender === username
                      ? "self-end bg-blue-500 text-white"
                      : "self-start bg-gray-200 text-black"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {message.sender !== username && (
                      <span className="flex gap-1 font-semibold">
                        {message.sender}
                      </span>
                    )}
                    <span className="text-xs text-muted-foreground">
                      {new Date().toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-sm">{message.content}</p>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>

        <div className="flex items-center gap-2">
          <Input
            placeholder="Type your message..."
            value={messageInput}
            onChange={(e) => setMessageInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isSending}
          />
          <Button
            onClick={handleSend}
            disabled={isSending || !messageInput.trim()}
          >
            <Send className={`h-4 w-4 ${isSending ? "animate-pulse" : ""}`} />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
