import { Router, Request, Response } from "express";

const router = Router();

// Required query params: creator, sheetname
// Returns a list of object(s)
router.get("/", (req: Request, res: Response) => {
  // TODO
});

export default router;
