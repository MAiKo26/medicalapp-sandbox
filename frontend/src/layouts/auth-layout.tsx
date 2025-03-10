import { ModeToggle } from "@/components/mode-toggle";
import { Outlet } from "react-router";

function AuthLayout() {
  return (
    <div>
      <div className="absolute right-4 top-4">
        <ModeToggle />
      </div>
      <Outlet />
    </div>
  );
}
export default AuthLayout;
