import { NextResponse, type NextRequest } from "next/server";

const protectedPrefixes = ["/settings", "/organizations", "/teams", "/sessions"];

export function proxy(request: NextRequest) {
  const isProtected = protectedPrefixes.some((prefix) => request.nextUrl.pathname.startsWith(prefix));
  const hasSession = request.cookies.has("vs_session");
  if (isProtected && !hasSession) {
    const url = request.nextUrl.clone();
    url.pathname = "/auth/signin";
    url.searchParams.set("next", request.nextUrl.pathname);
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/settings/:path*", "/organizations/:path*", "/teams/:path*", "/sessions/:path*"],
};