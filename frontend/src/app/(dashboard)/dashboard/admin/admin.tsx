import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { User } from "@/interfaces/user-interface";
import { env } from "@/config/env";

import { toast } from "@/hooks/use-toast";

export default function AdminDashboard() {
  const [searchTerm, setSearchTerm] = useState("");
  const [newUser, setNewUser] = useState({
    fullname: "",
    password: "",
    email: "",
    role: "",
  });

  const [users, setUsers] = useState<User[]>([]);
  useEffect(() => {
    const fetchUsers = async () => {
      const response = await fetch(`${env.VITE_API_URL}/users`);

      const data = await response.json();
      console.log(data);

      setUsers(data);
    };
    fetchUsers();
  }, []);

  const filteredPatients = users
    .filter((user) => user?.role === "patient")
    .filter(
      (user) =>
        user?.fullname?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user?.email?.toLowerCase().includes(searchTerm.toLowerCase()),
    );

  const filteredDoctors = users
    .filter((user) => user?.role === "doctor")
    .filter(
      (user) =>
        user?.fullname?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user?.email?.toLowerCase().includes(searchTerm.toLowerCase()),
    );

  const handleAddUser = async () => {
    try {
      console.log("Form values:", newUser);

      const response = await fetch(`${env.VITE_API_URL}/auth/register`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newUser),
      });
      if (!response.ok) {
        toast({
          title: "Registration failed",
          description: "Please try again.",
          variant: "destructive",
        });
      }
      console.log("Registration successful:", response);
    } catch (error) {
      console.error("Registration error:", error);
    }

    setNewUser({ fullname: "", email: "", password: "", role: "" });
  };

  const handleDeleteUser = async (email: string) => {
    try {
      const response = await fetch(`${env.VITE_API_URL}/users/${email}`, {
        method: "DELETE",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        toast({
          title: "Delete failed",
          description: "Could not delete user.",
          variant: "destructive",
        });
        return;
      }

      setUsers(users.filter((user) => user.email !== email));
      toast({
        title: "Success",
        description: "User deleted successfully.",
      });
    } catch (error) {
      console.error("Delete error:", error);
      toast({
        title: "Error",
        description: "An error occurred while deleting the user.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="w-full py-10">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
      </div>

      <div className="mb-6">
        <Input
          placeholder="Search patients or doctors..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <Tabs defaultValue="patient">
        <TabsList>
          <TabsTrigger value="patient">Patients</TabsTrigger>
          <TabsTrigger value="doctor">Doctors</TabsTrigger>
        </TabsList>

        <TabsContent value="patient">
          <Card>
            <CardHeader>
              <CardTitle>User Management</CardTitle>
              <CardDescription>Manage user accounts and roles</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Password</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow className="bg-muted/50">
                    <TableCell>
                      <Input
                        placeholder="Enter name"
                        value={newUser.fullname}
                        onChange={(e) =>
                          setNewUser({ ...newUser, fullname: e.target.value })
                        }
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        placeholder="Enter email"
                        value={newUser.email}
                        onChange={(e) =>
                          setNewUser({ ...newUser, email: e.target.value })
                        }
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        placeholder="Enter Password"
                        value={newUser.password}
                        onChange={(e) =>
                          setNewUser({ ...newUser, password: e.target.value })
                        }
                      />
                    </TableCell>
                    <TableCell>
                      <Select
                        value={newUser.role}
                        onValueChange={(value: string) =>
                          setNewUser({ ...newUser, role: value })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select role" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="patient">Patient</SelectItem>
                          <SelectItem value="doctor">Doctor</SelectItem>
                        </SelectContent>
                      </Select>
                    </TableCell>
                    <TableCell>
                      <Button
                        onClick={handleAddUser}
                        variant="default"
                        size="sm"
                      >
                        Add User
                      </Button>
                    </TableCell>
                  </TableRow>
                  {filteredPatients.map((user) => (
                    <TableRow key={user.email}>
                      <TableCell>{user.fullname}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell></TableCell>
                      <TableCell>{user.role}</TableCell>
                      <TableCell className="flex w-full items-center justify-center gap-2">
                        <Button disabled variant="outline" size="sm">
                          Edit
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDeleteUser(user.email)}
                        >
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="doctor">
          <Card>
            <CardHeader>
              <CardTitle>User Management</CardTitle>
              <CardDescription>Manage user accounts and roles</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Password</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow className="bg-muted/50">
                    <TableCell>
                      <Input
                        placeholder="Enter name"
                        value={newUser.fullname}
                        onChange={(e) =>
                          setNewUser({ ...newUser, fullname: e.target.value })
                        }
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        placeholder="Enter email"
                        value={newUser.email}
                        onChange={(e) =>
                          setNewUser({ ...newUser, email: e.target.value })
                        }
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        placeholder="Enter Password"
                        value={newUser.password}
                        onChange={(e) =>
                          setNewUser({ ...newUser, password: e.target.value })
                        }
                      />
                    </TableCell>
                    <TableCell>
                      <Select
                        value={newUser.role}
                        onValueChange={(value: string) =>
                          setNewUser({ ...newUser, role: value })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select role" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Admin">Admin</SelectItem>
                          <SelectItem value="Participant">
                            Participant
                          </SelectItem>
                        </SelectContent>
                      </Select>
                    </TableCell>
                    <TableCell className="flex w-full items-center justify-center">
                      <Button
                        onClick={handleAddUser}
                        variant="default"
                        size="sm"
                      >
                        Add User
                      </Button>
                    </TableCell>
                  </TableRow>
                  {filteredDoctors.map((user) => (
                    <TableRow key={user.email}>
                      <TableCell>{user.fullname}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell></TableCell>
                      <TableCell>{user.role}</TableCell>
                      <TableCell className="flex w-full items-center justify-center gap-2">
                        <Button disabled variant="outline" size="sm">
                          Edit
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDeleteUser(user.email)}
                        >
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
