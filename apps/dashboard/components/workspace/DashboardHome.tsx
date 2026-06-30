import { ActivityFeed, DashboardGrid, EmptyStateGallery, ErrorPreview, LoadingPreview, OnboardingChecklist, QuickActions, StatisticCards, SystemStatus, UsageOverview, WelcomeCard } from "./DashboardWidgets";

export function DashboardHome() {
  return <div className="ws-dashboard-home"><WelcomeCard /><StatisticCards /><DashboardGrid><UsageOverview /><ActivityFeed /><OnboardingChecklist /><QuickActions /><SystemStatus /><EmptyStateGallery /><LoadingPreview /><ErrorPreview /></DashboardGrid></div>;
}