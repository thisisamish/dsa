import {
  CLEANED_DATA_DIR,
  DEDUPED_DATA_DIR,
  filePathMap,
} from "../config/constants";
import {
  FilePathMap,
  SheetCreator,
  SheetName,
  SheetNamesByCreator,
} from "../types/sheetTypes";
import path from "path";

function getCleanedFilePath<C extends SheetCreator>(
  creator: C,
  sheetName: SheetNamesByCreator<C>
): string {
  const fileName = filePathMap[creator][sheetName] as string;
  return path.join(CLEANED_DATA_DIR, creator, fileName);
}

function getDedupedFilePath<C extends SheetCreator>(
  creator: C,
  sheetName: SheetNamesByCreator<C>
): string {
  const fileName = filePathMap[creator][sheetName] as string;
  return path.join(DEDUPED_DATA_DIR, creator, fileName);
}

export { getCleanedFilePath, getDedupedFilePath };
