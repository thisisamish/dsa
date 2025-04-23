import express, { Request, Response } from "express";
import fs from "fs";
import cors from "cors";
import swaggerUi from "swagger-ui-express";

import swaggerSpec from "./swagger";

import { getCleanedFilePath, getDedupedFilePath } from "./utils/utils";

import dupesRoutes from "./routes/dupesRoutes";
import itemsRoutes from "./routes/itemsRoutes";
import sheetsRoutes from "./routes/itemsRoutes";

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.use("/api/dupes", dupesRoutes);
// app.use("/api/items", itemsRoutes);
// app.use("/api/sheets", sheetsRoutes);

// app.use("/api/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// app.get("/api/:creator/:sheetname", (req, res) => {
//   const { creator, sheetname } = req.params;
//   const filePath = getCleanedFilePath(creator, sheetname);

//   if (!filePath || !fs.existsSync(filePath)) {
//     return res.status(404).json({ error: "Data file not found" });
//   }

//   try {
//     const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));
//     res.json(data);
//   } catch (err) {
//     res.status(500).json({ error: "Failed to read data file" });
//   }
// });

// app.post("/api/:sheetname", (req, res) => {
//   const newData = req.body;
//   fs.writeFileSync(CHECKPOINT_FILE, JSON.stringify(newData, null, 2));
//   res.json({ message: "Saved successfully" });
// });

app.listen(PORT, () => {
  console.log(`API Server running at http://localhost:${PORT}`);
  console.log(`Swagger docs at http://localhost:${PORT}/api/docs`);
});
