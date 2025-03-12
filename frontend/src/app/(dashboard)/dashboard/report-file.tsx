import ReportComponent from "@/components/file-report";
import { FileUploader } from "@/components/file-uploader";
import { Button } from "@/components/ui/button";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  Form,
} from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

// import { toast } from "sonner";

const schema = z.object({
  images: z.array(z.instanceof(File)),
});

type Schema = z.infer<typeof schema>;

const FileReport = () => {
  const [loading, setLoading] = useState(false);
  const [isUploading, setisUploading] = useState(false);
  const [canUpload, setCanUpload] = useState(false);

  const form = useForm<Schema>({
    resolver: zodResolver(schema),
    defaultValues: {
      images: [],
    },
  });

  function onSubmit(input: Schema) {
    setLoading(true);
    setisUploading(true);

    console.log(input);
    console.log(canUpload);

    // implement in public

    setLoading(false);
    setisUploading(false);
  }

  return (
    <div className="grid h-screen w-full">
      <ReportComponent />

      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex w-full flex-col gap-6"
        >
          <FormField
            control={form.control}
            name="images"
            render={({ field }) => (
              <div className="space-y-6">
                <FormItem className="w-full">
                  <FormLabel>Images</FormLabel>
                  <FormControl>
                    <FileUploader
                      value={field.value}
                      onValueChange={field.onChange}
                      maxFileCount={4}
                      maxSize={4 * 1024 * 1024}
                      setCanUpload={setCanUpload}
                      // pass the onUpload function here for direct upload
                      // onUpload={uploadFiles}
                      disabled={isUploading}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </div>
            )}
          />
          <Button className="w-fit" disabled={loading || !canUpload}>
            Save
          </Button>
        </form>
      </Form>
    </div>
  );
};

export default FileReport;
