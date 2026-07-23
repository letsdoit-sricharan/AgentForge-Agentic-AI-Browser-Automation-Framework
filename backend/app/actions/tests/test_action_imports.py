"""
Tests the public Action Library API.
"""

from app.actions import (
    BackAction,
    BlurAction,
    CheckAction,
    ClearAction,
    ClickAction,
    DoubleClickAction,
    FillAction,
    FocusAction,
    ForwardAction,
    HoverAction,
    NavigateAction,
    RefreshAction,
    RightClickAction,
    SelectOptionAction,
    UncheckAction,
    WaitAction,
)


def test_imports():

    print("\n==============================")
    print(" Action Library Import Test ")
    print("==============================\n")

    actions = [
        BackAction,
        ForwardAction,
        NavigateAction,
        RefreshAction,
        WaitAction,
        ClickAction,
        DoubleClickAction,
        RightClickAction,
        HoverAction,
        FillAction,
        ClearAction,
        CheckAction,
        UncheckAction,
        SelectOptionAction,
        FocusAction,
        BlurAction,
    ]

    for action in actions:
        print(f"✓ {action.__name__}")

    print("\n✅ All Action Library imports are valid.")


if __name__ == "__main__":
    test_imports()
