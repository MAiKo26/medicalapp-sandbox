import { useChat } from "ai/react";
import { CornerDownLeft, Loader2, TextSearch } from "lucide-react";
import Markdown from "./markdown";
import Messages from "./messages";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "./ui/accordion";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";

type Props = {
  reportData?: string;
};

const ChatComponent = ({ reportData }: Props) => {
  const { messages, input, handleInputChange, handleSubmit, isLoading, data } =
    useChat({
      api: "api/medichatgemini",
    });
  return (
    <div className="relative flex h-full min-h-[50vh] flex-col gap-4 rounded-xl bg-muted/50 p-4">
      <Badge
        variant={"outline"}
        className={`absolute right-3 top-1.5 ${reportData && "bg-[#00B612]"}`}
      >
        {reportData ? "✓ Report Added" : "No Report Added"}
      </Badge>
      <div className="flex-1" />
      <Messages messages={messages} isLoading={isLoading} />
      {data?.length !== undefined && data.length > 0 && (
        <Accordion type="single" className="text-sm" collapsible>
          <AccordionItem value="item-1">
            <AccordionTrigger dir="">
              <span className="flex flex-row items-center gap-2">
                <TextSearch /> Relevant Info
              </span>
            </AccordionTrigger>
            <AccordionContent className="whitespace-pre-wrap">
              <Markdown
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                text={(data[data.length - 1] as any).retrievals as string}
              />
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      )}
      <form
        className="relative overflow-hidden rounded-lg border bg-background"
        onSubmit={(event) => {
          event.preventDefault();
          handleSubmit(event, {
            data: {
              reportData: reportData as string,
            },
          });
        }}
      >
        <Textarea
          value={input}
          onChange={handleInputChange}
          placeholder="Type your query here..."
          className="min-h-12 resize-none border-0 p-3 shadow-none focus-visible:ring-0"
        />
        <div className="flex items-center p-3 pt-0">
          <Button
            disabled={isLoading}
            type="submit"
            size="sm"
            className="ml-auto"
          >
            {isLoading ? "Analysing..." : "3. Ask"}
            {isLoading ? (
              <Loader2 className="size-3.5 animate-spin" />
            ) : (
              <CornerDownLeft className="size-3.5" />
            )}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default ChatComponent;
