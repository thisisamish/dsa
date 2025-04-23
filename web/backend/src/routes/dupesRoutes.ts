import { Router, Request, Response } from "express";
import path from "path";
import fs from "fs";

const router = Router();

const DEDUPED_DATA_DIR = path.join(
  __dirname,
  "..",
  "..",
  "..",
  "..",
  "data",
  "deduped-data"
);

const DUPES_DATA_DIR = path.join(
  __dirname,
  "..",
  "..",
  "..",
  "..",
  "data",
  "data-deduping"
);

interface Item {
  url: string;
  expanded_url: string;
  expanded_stripped_url: string;
  original_title?: string;
  step_title?: string;
  sub_step_title?: string;
  type: string;
  id_base: string;
  id: string;
  title: string;
  platform: string;
  description?: string;
}

interface DupesData {
  [creator: string]: {
    [sheetname: string]: {
      dupes_data: Item[][];
      total_items_with_dupes: number;
      total_dupes: number;
      total_items_in_sheet_before_dedupe: number;
      total_items_in_sheet_after_dedupe: number;
    };
  };
}

// WARNING: This is a very dev-oriented route used only for internal purpose. Hence, no error-handling or validation is done.
// Required query params: creator, sheetname
// Returns a list of lists of objects: [[{item1_dupe1}, {item1_dupe2},...], [item2_dupe1,...],...]
router.get("/", (req: Request, res: Response): any => {
  const creator = req.query.creator as string;
  const sheetname = req.query.sheetname as string;
  if (creator === undefined || sheetname == undefined) {
    return res
      .status(400)
      .json({ error: "Please use creator and sheetname query params." });
  }
  console.log(`creator: ${creator}; sheetname: ${sheetname}`);
  const dupesPath = path.join(DUPES_DATA_DIR, "dupes_data_all_sheets.json");
  console.log(`dupesPath: ${dupesPath}`);
  if (!dupesPath || !fs.existsSync(dupesPath)) {
    return res.status(404).json({ error: "Data file not found" });
  }

  try {
    const data: DupesData = JSON.parse(fs.readFileSync(dupesPath, "utf-8"));
    const dupesData = data[creator][sheetname];
    res.status(200).json(dupesData);
  } catch (err) {
    console.log(`Failed to read data file: ${err}`);
    res.status(500).json({ error: "Failed to read data file" });
  }
});

// WARNING: This is a very dev-oriented route used only for internal purpose. Hence, no error-handling or validation is done.
// Required query params: creator, sheetname
// Required body of type Item
// Deletes every Item with id of the Item in body
// Adds new Item (the Item in body)
// Returns the newly created Item
router.post("/resolve", (req: Request, res: Response): any => {
  const creator = req.body.creator;
  const sheetname = req.body.sheetname;
  const newItem: Item = req.body.resolvedItem;

  const sheetPath = path.join(DEDUPED_DATA_DIR, creator, sheetname + ".json");

  if (!sheetPath || !fs.existsSync(sheetPath)) {
    return res.status(404).json({ error: "Data file not found" });
  }

  let data: Item[] = [];

  try {
    data = JSON.parse(fs.readFileSync(sheetPath, "utf-8"));
  } catch (err) {
    console.log(`Failed to read data file: ${err}`);
    res.status(500).json({ error: "Failed to read data file" });
  }

  const newData = data.filter((item) => item.id != newItem.id);
  newData.push(newItem);

  try {
    fs.writeFileSync(sheetPath, JSON.stringify(newData, null, 2));
    res.status(201).json(newItem);
  } catch (err) {
    console.log(`Failed to write data file: ${err}`);
    res.status(500).json({ error: "Failed to write data file" });
  }

  res.status(200).json();
});

export default router;
