export const researchTopicLabels = {
  "air-quality": "Air Quality",
  agriculture: "Agriculture",
  aquaculture: "Aquaculture",
  bathymetry: "Bathymetry",
  biodiversity: "Biodiversity",
  "climate-change": "Climate Change",
  "coral-reefs": "Coral Reefs",
  fisheries: "Fisheries",
  flooding: "Flooding",
  "land-cover": "Land Cover",
  lidar: "LiDAR",
  mangroves: "Mangroves",
  "pm2-5": "PM2.5",
  seagrass: "Seagrass",
  "water-quality": "Water Quality",
} as const;

export const topicLabel = (topic: string) =>
  researchTopicLabels[topic as keyof typeof researchTopicLabels] ?? topic;
