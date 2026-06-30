export type AuthFormState = {
  status: "idle" | "loading" | "success" | "error";
  message?: string;
};

export const authCopy = {
  signin: {
    title: "Sign in to VoiceSense",
    description: "Manage AI employees, conversations, tools, and teams from one secure workspace.",
  },
  signup: {
    title: "Create your VoiceSense workspace",
    description: "Start with an organization, invite your team, and build your first AI employee when you are ready.",
  },
  forgot: {
    title: "Reset your password",
    description: "Enter your account email and we will send secure reset instructions if the account exists.",
  },
  reset: {
    title: "Choose a new password",
    description: "Use a strong password with at least 12 characters.",
  },
  verify: {
    title: "Verify your email",
    description: "Confirm your email address to protect your workspace and unlock production features.",
  },
};

export function validateEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export async function simulateAuthRequest(successMessage: string): Promise<AuthFormState> {
  await new Promise((resolve) => setTimeout(resolve, 450));
  return { status: "success", message: successMessage };
}