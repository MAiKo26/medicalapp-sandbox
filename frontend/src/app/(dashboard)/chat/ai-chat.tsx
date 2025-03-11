import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { env } from "@/config/env";
import { useChat } from "@ai-sdk/react";
import { Bot, Ellipsis, Send } from "lucide-react";
import ReactMarkdown from "react-markdown";

export default function AiChat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } =
    useChat({
      api: `${env.VITE_API_URL}/ws/chat/ai-chat`,
      streamProtocol: "text",
      onResponse: (response) => {
        console.log(response);
      },
      onError: (response) => {
        console.log(response);
      },
    });

  return (
    <Card className="h-[calc(100vh-7rem)]">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bot className="h-6 w-6" /> AI Assistant
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <ScrollArea className="h-[calc(100vh-16rem)] rounded-lg border p-4">
          <div className="space-y-4">
            {messages.map((message, index) => {
              const parts = message.content.split("</think>");
              const thought =
                parts.length > 1
                  ? parts[0].replace("<think>", "").trim()
                  : null;
              const response =
                parts.length > 1 ? parts[1].trim() : parts[0].trim();

              return (
                <div
                  key={index}
                  className={`flex items-start gap-4 ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[75%] space-y-2 rounded-lg p-3 ${
                      message.role === "user"
                        ? "ml-auto bg-primary text-primary-foreground"
                        : "bg-muted"
                    }`}
                  >
                    <div className="flex items-center gap-2 text-sm">
                      {message.role === "assistant" && (
                        <Bot className="h-4 w-4" />
                      )}
                      <span className="font-semibold">
                        {message.role === "user" ? "You" : "AI"}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {new Date().toLocaleTimeString()}
                      </span>
                    </div>
                    {thought && (
                      <blockquote className="border-l-4 border-gray-500 bg-gray-100 p-2 text-sm text-gray-700">
                        <ReactMarkdown>{`**AI Thought Process:**\n${thought}`}</ReactMarkdown>
                      </blockquote>
                    )}
                    <div className="text-left text-sm">
                      <ReactMarkdown>{response}</ReactMarkdown>
                    </div>
                  </div>
                </div>
              );
            })}
            {isLoading && (
              <div className="flex justify-start">
                <Ellipsis className="h-6 w-6 animate-bounce" />
              </div>
            )}
          </div>
        </ScrollArea>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            placeholder="Type your message..."
            value={input}
            onChange={handleInputChange}
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading || !input.trim()}>
            <Send className={`h-4 w-4 ${isLoading ? "animate-pulse" : ""}`} />
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
