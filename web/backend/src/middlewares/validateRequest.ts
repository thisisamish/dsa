import { ZodSchema } from "zod";
import { Request, Response, NextFunction } from "express";

export function validateRequest({
  body,
  query,
  params,
}: {
  body?: ZodSchema,
  query?: ZodSchema,
  params?: ZodSchema,
}) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      if (body) req.body = body.parse(req.body);
      if (query) req.query = query.parse(req.query);
      if (params) req.params = params.parse(req.params);
      next();
    } catch (err) {
      if (err instanceof Error) {
        return res.status(400).json({
          error: err.name,
          message: err.message,
          details: err,
        });
      }
      return res.status(400).json({ error: "Invalid request", details: err });
    }
  };
}
