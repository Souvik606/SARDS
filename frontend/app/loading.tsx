import { Loader } from "lucide-react";

export default function Loading() {
  // Or a custom loading skeleton component
  return (
    <div className="flex items-center justify-center p-5">
      <Loader className="size-10 animate-spin" />
    </div>
  );
}
