import { z } from "zod";

const sheetQueryParamsSchema = z.object({
  creator: z.string(),
  sheetname: z.string(),
});
