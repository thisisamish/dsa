from enum import Enum


class TutorialPlatform(str, Enum):
    GFG = "GFG"
    PROGRAMIZ = "PROGRAMIZ"
    SCALER = "SCALER"
    CODE360 = "C360"
    YOUTUBE = "YT"
    UNKNOWN = ""


class ProblemPlatform(str, Enum):
    LEETCODE = "LC"
    NEETCODE = "NC"
    GFG = "GFG"
    CODE360 = "C360"
    INTERVIEWBIT = "IB"
    CODECHEF = "CC"
    CODEFORCES = "CF"
    ATCODER = "AC"
    TOPCODER = "TC"
    CSES = "CSES"
    LINTCODE = "LINT"
    SPOJ = "SPOJ"
    HACKEREARTH = "HE"
    HACKERRANK = "HR"
    UNKNOWN = ""
