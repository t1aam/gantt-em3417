```mermaid
gantt
    title Kế hoạch lắp ráp sản phẩm R
    dateFormat HH
    axisFormat %H

    section Cụm đơn
    C1 (8h, 1CN) :a1, 0, 8
    C2 (8h, 1CN) :a2, 0, 8
    C3 (10h,1CN):a3, 0, 10
    C4 (4h, 1CN) :a4, 0, 4
    C5 (5h, 1CN) :a5, 0, 5

    section Cụm phức trung gian
    B1 (2h, 2CN) :b1, after a1 a2, 2
    B2 (6h, 1CN) :b2, after a1 b1, 6
    B3 (9h, 2CN) :b3, after b1 a3, 9

    section Lắp & hoàn thiện
    R (5h, 2CN)  :r1, after b1 b2 b3 a4 a5, 5
    Hoàn thiện (2h,1CN) :r2, after r1, 2
