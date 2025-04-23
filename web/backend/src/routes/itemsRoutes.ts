import { Router, Request, Response } from "express";

const router = Router();

/**
 * @swagger
 * /api/{creator}/{sheetname}:
 *   get:
 *     summary: Get full sheet data for a specific creator and sheet
 *     parameters:
 *       - in: path
 *         name: creator
 *         required: true
 *         schema:
 *           type: string
 *         description: The creator's name (e.g. striver, lb)
 *       - in: path
 *         name: sheetname
 *         required: true
 *         schema:
 *           type: string
 *         description: The name of the sheet (e.g. 75, 150)
 *     responses:
 *       200:
 *         description: Successfully retrieved sheet data
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *       404:
 *         description: Sheet not found
 */
// Required query params: creator, sheetname
// Returns a list of object(s)
router.get("/:id", (req: Request, res: Response) => {
  // TODO
});

// Required query params: creator, sheetname
// Updates/adds a single item by id, returns error if multiple items with same id exist
// Returns the object updated/added
router.post("/:id", (req: Request, res: Response) => {
  // TODO
});

// Required query params: creator, sheetname
// Deletes object(s) matching the id
// Returns the object deleted
router.delete("/:id", (req: Request, res: Response) => {
  // TODO
});

export default router;
