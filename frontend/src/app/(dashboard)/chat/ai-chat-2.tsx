import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { env } from "@/config/env";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { useState } from "react";
// import { z } from "zod";

// export const exampleMetadataSchema = z.object({
//   duration: z.number().optional(),
//   model: z.string().optional(),
//   totalTokens: z.number().optional(),
// });

// export type ExampleMetadata = z.infer<typeof exampleMetadataSchema>;

function AiChat2() {
  const [input, setInput] = useState("");

  const { messages, sendMessage } = useChat({
    transport: new DefaultChatTransport({
      api: `${env.VITE_API_URL}/ws/chat/custom-ai-chat-protocol-data`,
    }),

    onFinish: (response) => {
      console.log(response);
    },
    onError: (response) => {
      console.log(response);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage({ text: input });
    setInput("");
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const renderJson = (data: any) => {
    try {
      return JSON.stringify(data, null, 2);
    } catch {
      return "Invalid JSON data";
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <Input
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <Button type="submit">Click me</Button>
      </form>
      <div>
        {messages.map(
          (message, index) =>
            message.role === "assistant" && (
              <div className="flex flex-col items-start gap-4" key={index}>
                <div>
                  <h1 className="text-4xl font-bold">This is role :</h1>
                  <div>{message.role}</div>
                </div>
                {/* <div>
                  <h1 className="text-4xl font-bold">This is content :</h1>
                  <div>{message.content}</div>
                </div> */}
                {/* <div>
                  <h1 className="text-4xl font-bold">This is annoations :</h1>
                  <div>
                    <div>
                      <strong>Annotations:</strong>{" "}
                      <pre>{renderJson(message)}</pre>
                    </div>
                  </div>
                </div> */}
                {/* <div>
                  <h1 className="text-4xl font-bold">This is id :</h1>
                  <div>{message.id}</div>
                </div> */}
                <div>
                  <h1 className="text-4xl font-bold">This is parts :</h1>
                  <div>
                    {message.parts.map((part, index) => {
                      switch (part.type) {
                        case "text":
                          return (
                            <div key={index}>
                              <div className="text-2xl">Text part:</div>
                              {part.text}
                            </div>
                          );
                        case "reasoning":
                          return (
                            <div key={index}>
                              <div className="text-2xl"> Reasoning parts :</div>
                              <div>{part.text}</div>
                            </div>
                          );
                        // case "source":
                        //   return (
                        //     <div key={index}>
                        //       Source is
                        //       {/* {(() => {
                        //         switch (part.type) {
                        //           case "source":
                        //             return (
                        //               <a href={part.source.id}>
                        //                 {part.source.id}
                        //                 {part.source.sourceType === "text" &&
                        //                   "heyoo"}
                        //               </a>
                        //             );
                        //           case "url":
                        //             return <span>{part.source.id}a</span>;
                        //           default:
                        //             return <span>Unknown Source Type</span>;
                        //         }
                        //       })()} */}
                        //     </div>
                        //   );
                        // case "tool-invocation":
                        //   return (
                        //     <div key={index}>
                        //       Tool Invocation{" "}
                        //       {part.toolInvocation.toolName}{" "}
                        //     </div>
                        //   );
                        case "data-search-status":
                          return (
                            <div>
                              Data Annotation : {JSON.stringify(part.data)}
                            </div>
                          );
                        default:
                          return null;
                      }
                    })}
                  </div>
                </div>
              </div>
            ),
        )}
      </div>
    </div>
  );
}
export default AiChat2;
